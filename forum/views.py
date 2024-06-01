from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Count

def forum_home(request):
    sections = Section.objects.all()
    return render(request, 'forum_home.html', {'sections': sections})

def section_detail(request, pk):
    section = get_object_or_404(Section, pk=pk)
    topics = section.topics.all()
    return render(request, 'section_detail.html', {'section': section, 'topics': topics})

#@login_required
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    posts = topic.posts.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = PostForm()
    return render(request, 'topic_detail.html', {'topic': topic, 'posts': posts, 'form': form})

#@login_required
def new_topic(request, section_pk):
    section = get_object_or_404(Section, pk=section_pk)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.section = section
            topic.created_by = request.user
            topic.save()
            return redirect('section_detail', pk=section.pk)
    else:
        form = TopicForm()
    return render(request, 'new_topic.html', {'form': form, 'section': section})

@csrf_exempt
def like_topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    user = request.user
    liked = False

    like, created = Like.objects.get_or_create(user=user, topic=topic)

    if not created:
        like.delete()
        topic.likes -= 1
    else:
        topic.likes += 1
        liked = True

    topic.save()
    return JsonResponse({'success': True, 'likes': topic.likes, 'liked': liked})

def user_profile(request):
    return render(request, 'user_profile.html')

def whats_new(request):
    latest_sections = Section.objects.order_by('-created_at')[:5]
    latest_topics = Topic.objects.order_by('-created_at')[:5]
    latest_posts = Post.objects.order_by('-created_at')[:5]
    latest_likes = Like.objects.order_by('-created_at')[:5]

    context = {
        'latest_sections': latest_sections,
        'latest_topics': latest_topics,
        'latest_posts': latest_posts,
        'latest_likes': latest_likes,
    }

    return render(request, 'whats_new.html', context)

def members(request):
    top_posters = User.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
    top_reactors = User.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    top_topic_creators = User.objects.annotate(topic_count=Count('topics')).order_by('-topic_count')[:5]
    
    context = {
        'top_posters': top_posters,
        'top_reactors': top_reactors,
        'top_topic_creators': top_topic_creators,
    }
    
    return render(request, 'members.html', context)