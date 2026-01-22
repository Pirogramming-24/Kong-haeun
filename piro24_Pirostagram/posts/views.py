from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Comment
from .forms import PostForm, CommentForm


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
    comments = post.comments.all()
    comment_form = CommentForm()

    context = {
        'post':post,
        'comments':comments,
        'comment_form': comment_form,
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

@login_required
def comment_create(request,pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect('posts:detail', pk=pk)

@login_required
def comment_update(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post_id=pk)

    if comment.author != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('posts:detail', pk=pk)
    else:
        form = CommentForm(instance=comment)

    context = {
        'post': comment.post,
        'comment_form': form,
        'editing_comment': comment,
        'comments': comment.post.comments.all(),
    }
    return render(request, 'posts/detail.html', context)
    
@login_required
def comment_delete(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.author != request.user:
        return HttpResponseForbidden()

    comment.delete()
    return redirect('posts:detail', pk=pk)