from django.shortcuts import render, redirect
from users.forms import SignupForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout

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
        return redirect('login')
    return render(request, 'users/logout.html')