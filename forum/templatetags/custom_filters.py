from django import template
from forum.models import Like

register = template.Library()

@register.filter
def is_liked(user, topic):
    return Like.objects.filter(user=user, topic=topic).exists()
