from django.urls import path
from .views import (BlogDetailView,BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView, ProfileView, BlogImage, SignUpView, ProfileUpdateView,add_comment)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User 
from . import views

app_name = 'blog'
urlpatterns = [
    # path('post/<int:pk>/delcmt/',views.delete_comment,name='delete-comment'),
    # path('post/<int:pk>/createcmt/',CommentView.as_view(),name='new_comment'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/delete/',BlogDeleteView.as_view(),name='post_delete'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/post_detail',BlogDetailView.as_view(), name='post_detail'),
    path('',BlogListView.as_view(), name='home'),
    path('post/',BlogImage.as_view(),name='image'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/edit/<int:pk>',ProfileUpdateView.as_view(), name='profile_edit'),                                                                                                                                                                                                                   
    path('profile/',ProfileView.as_view(),name='profile'),
    path("post/comment/<int:pk>/",views.add_comment,name='comment'),
    path('sendmail/',views.sendMail,name='email'),
]   

