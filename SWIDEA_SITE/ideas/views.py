from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Idea, IdeaStar
from .forms import IdeaForm
from django.views.decorators.http import require_POST

# Create your views here.
def idea_list(request):
    sort = request.GET.get('sort', 'latest')

    if sort == 'title':
        ideas = Idea.objects.order_by('title')
    elif sort == 'interest':
        ideas = Idea.objects.order_by('-interest')
    else:
        ideas = Idea.objects.order_by('-created_at')

    session_key = request.session.session_key
    starred_ids = []
    if session_key:
        starred_ids = IdeaStar.objects.filter(
            session_key=session_key
        ).values_list('idea_id', flat=True)

    context = {
        'ideas': ideas,
        'favorites': starred_ids,
        'sort': sort,
    }
    return render(request, 'ideas/idea_list.html', context)


def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ideas:list')
    else:
        form = IdeaForm()
    context = {
        'form':form,
        'mode':'create',
    }
    return render(request,'ideas/idea_form.html',context)

def idea_detail(request,pk):
    idea = Idea.objects.get(id=pk)
    session_key = request.session.session_key

    # 찜 여부 판단
    is_favorite = IdeaStar.objects.filter(
        idea=idea,
        session_key=session_key
    ).exists()

    context = {
        'idea': idea,
        'is_favorite': is_favorite
    }
    return render(request,'ideas/idea_detail.html',context)

def idea_update(request,pk):
    idea = Idea.objects.get(id=pk)
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('ideas:detail', pk=pk)
    else:
        form = IdeaForm(instance=idea)
    context={
        'form':form,
        'mode':'update',
    }
    return render(request,'ideas/idea_form.html',context)

def idea_delete(request,pk):
    if request.method == "POST":
        idea = Idea.objects.get(id=pk)
        idea.delete()
    return redirect('ideas:list')

def idea_favorite(request, pk):
    idea = Idea.objects.get(id=pk)
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    star, created = IdeaStar.objects.get_or_create(
        idea=idea,
        session_key=session_key
    )

    if not created:
        star.delete()  # 이미 찜 -> 해제

    return redirect(request.META.get('HTTP_REFERER', 'ideas:list'))

@require_POST
def idea_interest(request, pk):
    idea = Idea.objects.get(id=pk)
    action = request.POST.get('action')

    if action == 'plus':
        idea.interest += 1
    elif action == 'minus':
        if idea.interest > 0:
            idea.interest -= 1

    idea.save()

    return JsonResponse({
        'interest': idea.interest
    })