from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
#    path('posts/', views.posts_list, name='posts_list'),
    path("posts/", views.PostListView.as_view(), name='post_list'),
   # path('posts/<int:id>/', views.posts_detail, name='posts_detail'),
    path('ticket', views.ticket, name='ticket'),
    path('posts/<pk>/', views.posts_detail, name="posts_detail"),
    path('posts/<post_id>/comment', views.post_comment, name="post_comment"),

    path('search', views.post_search, name='post_search'),



]