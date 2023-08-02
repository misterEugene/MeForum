from django.contrib import admin
from forum.models import *


@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password')
    
@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'description', 'slug'
    prepopulated_fields = {"slug": ('name',)}
    
@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = 'title', 'content', 'create_time', 'update_time', 'cat_id', 'author_id', 'is_published', 'is_allow_comments'
    list_editable = 'is_allow_comments', 'is_published'
    list_filter = 'is_published', 'create_time', 'update_time', 'likes', 'dislikes', 'views', 'is_allow_comments'
    
@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_editable = 'is_approved',
    list_display =  'content', 'create_time', 'update_time', 'author_id', 'is_approved'