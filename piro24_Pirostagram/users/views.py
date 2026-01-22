from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from users.forms import SignupForm, LoginForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Follow

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:feed')
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'users/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('posts:feed')
        else:
            context = {
                'form':form,
            }
            return render(request, 'users/login.html',context)

    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'users/login.html', context)

@login_required
def logout(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('users:login')
    return render(request, 'users/logout.html')

@login_required
def follow_toggle(request, user_id):
    to_user = get_object_or_404(User, pk=user_id)

    # 자기 자신은 팔로우 X
    if request.user == to_user:
        return redirect('posts:feed')

    follow, created = Follow.objects.get_or_create(
        from_user=request.user,
        to_user=to_user
    )

    if not created: # 이미 팔로우 중인지
        follow.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()

    is_following = False
    if profile_user != request.user:
        is_following = Follow.objects.filter(
            from_user=request.user,
            to_user=profile_user
        ).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile', request.user.username)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'users/profile_edit.html', context)