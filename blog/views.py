from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone

from .models import Post
from .forms import PostForm, DeleteForm

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
	
	if post.author == request.user:	
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
	else:
		"""
		return render(request, 'blog/post_detail.html', {
                'post': post,
                'error_message': "You are not the post author.",
            })
        """
		return HttpResponse("You are not the post author.", content_type="text/plain")

	return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
	
	post_to_delete = get_object_or_404(Post, pk=pk)
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	
	# process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = DeleteForm(request.POST)
		# check whether it's valid
		if form.is_valid():
			# access the form data
			selection = form.cleaned_data['yes_no']
			# check if 'Yes' condition
			if selection == 'True':
				# delete the post
				Post.objects.filter(pk=pk).delete()
				return redirect('/blog/')
			# if 'No' condition
			else:
				# send to blog index page
				return redirect('/blog/')
	else:
		form = DeleteForm()	
	return render(request, 'blog/post_delete.html', {'form': form})
	
	"""
	if post_to_delete.author == request.user:
		Post.objects.filter(pk=pk).delete()
	else:
		return HttpResponse("You are not the post author.", content_type="text/plain")
	return render(request, 'blog/index.html', {'posts':posts})
	"""
