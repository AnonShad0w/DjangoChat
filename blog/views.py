from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import Post
from .forms import PostForm

def post_list(request):
	
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, pk):
	
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})
	
def post_new(request):
	
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.localtime(timezone.now())
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})
	
def post_edit(request, pk):
	
	post = get_object_or_404(Post, pk=pk)
		
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.localtime(timezone.now())
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
	
	post_to_delete = get_object_or_404(Post, pk=pk)
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

	if post_to_delete.author == request.user:
		Post.objects.filter(pk=pk).delete()
	else:
		return HttpResponse("This post was not created by you.", content_type="text/plain")

	return render(request, 'blog/index.html', {'posts':posts})
