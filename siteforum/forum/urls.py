from forum.views import *
from django.urls import path

urlpatterns = [
    path("", index, name="home"),
    path("category/<slug:cat_slug>/", category, name="category"),
    path("post/<int:post_id>/", post, name="post"),
    path("addpage/", addPage, name="addpage"),
    path("about/", about, name="about"),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register'),    
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),    
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),   
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),  
    path('comment/<int:post_id>/<int:comment_id>/delete/', delete_comment, name='delete_comment'), 
    path('post/<int:post_id>/like', like_post, name='like_post'),
    path('post/<int:post_id>/dislike', dislike_post, name='dislike_post'),
    path('comment/<int:comment_id>/like', like_comment, name='like_comment'),
    path('comment/<int:comment_id>/dislike', dislike_comment, name='dislike_comment'),
]
