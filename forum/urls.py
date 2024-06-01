from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('section/<int:pk>/', views.section_detail, name='section_detail'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('section/<int:section_pk>/new/', views.new_topic, name='new_topic'),
    path('like/<int:topic_id>/', views.like_topic, name='like_topic'),
    path('profile/', views.user_profile, name='user_profile'),  
    path('whats-new/', views.whats_new, name='whats_new'), 
    path('members/', views.members, name='members'), 
]
