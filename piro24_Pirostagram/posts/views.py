from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post
from .forms import PostForm


# Create your views here.
@login_required
def feed(request):
    posts = Post.objects.all()
    context = {
        "posts":posts,
    }
    return render(request,"posts/feed.html",context)

@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:detail', pk=post.pk)
    else:
        form = PostForm()
    
    context = {
        'form':form,
    }
    return render(request, 'posts/create.html',context)

@login_required
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    context = {
        'post':post,
    }
    return render(request, 'posts/detail.html', context)

@login_required
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form':form,
    }

    return render(request, 'posts/update.html', context)

@login_required
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        post.delete()
        return redirect('posts:feed')

    return HttpResponseForbidden()

def home(request):
    # 로그인 되어 있으면 피드로
    if request.user.is_authenticated:
        return redirect('posts:feed')

    # 로그인 안 된 경우 메인 화면
    return render(request, 'posts/home.html')