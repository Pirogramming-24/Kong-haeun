from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Comment, Like, Story
from .forms import PostForm, CommentForm
from users.models import Follow
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required
def feed(request):
    # 내가 팔로우한 사람들 id 목록
    following_users = Follow.objects.filter(
        from_user=request.user
    ).values_list('to_user', flat=True)

    # 스토리
    all_stories = Story.objects.filter(
        author__in=list(following_users) + [request.user],
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('created_at')

    story_map = {}
    for story in all_stories:
        if story.author_id not in story_map:
            story_map[story.author_id] = story

    stories = story_map.values()

    # 나 + 팔로우한 사람들의 게시글
    posts = Post.objects.filter(
        author__in=list(following_users) + [request.user]
    ).distinct()
    
    # 좋아요
    liked_post_ids = Like.objects.filter(
        user=request.user,
        post__in=posts
    ).values_list('post_id', flat=True)

    context = {
        "stories": stories,
        "posts":posts,
        'liked_post_ids': liked_post_ids,
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
    is_liked= post.likes.filter(user=request.user).exists()

    context = {
        'post':post,
        'comments':comments,
        'comment_form': comment_form,
        'is_liked':is_liked,
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

@login_required
def like_toggle(request, pk):
    post = get_object_or_404(Post, pk=pk)

    like = Like.objects.filter(
        user=request.user,
        post=post
    )

    if like.exists():
        like.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=post
        )
    
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))

@login_required
def story_create(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')

        for image in images:
            Story.objects.create(
                author=request.user,
                image=image
            )

        return redirect('posts:feed')

    return render(request, 'posts/story_create.html')

@login_required
def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)

    stories = Story.objects.filter(
        author=story.author,
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('created_at')

    return render(request, 'posts/story_detail.html', {
        'stories': stories,
        'start_story': story,
    })