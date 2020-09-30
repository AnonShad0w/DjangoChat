from django.urls import path
from . import views

#app_name = 'blog'
urlpatterns = [
	path('', views.post_list, name='index'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
	path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
	path('post/<int:pk>/new-comment/', views.new_comment, name='new_comment'),
	path('post/<int:pk>/<int:comment_id>/edit-comment/', views.edit_comment, name='edit_comment'),
	path('post/<int:pk>/delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]
