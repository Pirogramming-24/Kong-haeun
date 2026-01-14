from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

import os
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage

from apps.posts.services.ocr_service import run_ocr
from apps.posts.services.nutrition_parser import parse_nutrition

# Create your views here.
def main(request):
    posts = Post.objects.all()

    search_txt = request.GET.get('search_txt')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_txt:
        posts = posts.filter(title__icontains=search_txt)  # 대소문자 구분 없이 검색
    
    try:
        if min_price:
            posts = posts.filter(price__gte=int(min_price))
        if max_price:
            posts = posts.filter(price__lte=int(max_price))
    except (ValueError, TypeError):
        pass  # 필터를 무시하되, 기존 검색 필터를 유지

    context = {
        'posts': posts,
        'search_txt': search_txt,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'posts/list.html', context=context)

def create(request):
    if request.method == 'GET':
        form = PostForm()
        context = { 'form': form }
        return render(request, 'posts/create.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/')

def detail(request, pk):
    target_post = Post.objects.get(id = pk)
    context = { 'post': target_post }
    return render(request, 'posts/detail.html', context=context)

def update(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        context = {
            'form': form, 
            'post': post
        }
        return render(request, 'posts/update.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:detail', pk=pk)

def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/')


def ocr_analyze(request):
    if request.method != "POST":
        return JsonResponse({"error": "invalid method"}, status=405)

    file = request.FILES.get("image")
    if not file:
        return JsonResponse({"error": "no image"}, status=400)

    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    saved_path = default_storage.save(f"uploads/{file.name}", file)
    full_path = os.path.join(settings.MEDIA_ROOT, saved_path)

    try:
        texts = run_ocr(full_path)
        nutrition = parse_nutrition(texts)
    finally:
        if os.path.exists(full_path):
            os.remove(full_path)

    return JsonResponse({
        "nutrition": nutrition,
    })