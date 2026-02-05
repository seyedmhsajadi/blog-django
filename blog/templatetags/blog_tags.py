from django import template
from ..models import Post, Comment
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe

register = template.Library()

#ایجاد نام مختصر مثلا در پایین tp
@register.simple_tag(name="tp")
def total_posts():
    return Post.published.count()

@register.simple_tag()
def total_commments():
    return Comment.objects.filter(active=True).count()

@register.simple_tag()
def last_post_date():
    return Post.published.last().publish

@register.simple_tag
def most_popular_posts(count=2):
    return Post.published.annotate(comment_count=Count('comments')).order_by('comment_count')[:count]

#unlike inclusion tags that return a template, simple tags just return string
@register.inclusion_tag("partials/latest_posts.html")
def latest_posts(count=4):
    l_posts = Post.published.order_by('-publish')[:count]
    context = {
        'l_posts': l_posts,
    }
    return context

@register.filter(name="markdown")
def to_markdown(text):
    return mark_safe(markdown(text))