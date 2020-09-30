from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'created_date', 'likes')
	
class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'created_date', 'likes')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
