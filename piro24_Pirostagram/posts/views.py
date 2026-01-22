from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post

# Create your views here.
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        "posts":posts,
    }
    return render(request,"posts/feed.html",context)