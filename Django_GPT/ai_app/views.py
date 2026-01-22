from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from ai_app.services.huggingface import (summarize_text, analyze_sentiment, generate_text)
from ai_app.models import ChatHistory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
def home(request):
    return render(request, "home.html", {"tab": None})

@login_required
@require_http_methods(["GET","POST"])
def summarize(request):
    result = None
    user_input=""

    if request.method == "POST":
        user_input = request.POST.get("text","")
        result = summarize_text(user_input)
        ChatHistory.objects.create(
                user=request.user,
                task="summarize",
                input_text=user_input,
                result_text=result,
            )     
    
    histories = ChatHistory.objects.filter(
        user=request.user,
        task="summarize"
    ).order_by("-created_at")[:5]

    context = {
        "tab":"summarize",
        "result":result,
        "histories": histories,
        "user_input": user_input,
    }

    return render(request, "summarize.html", context)

@login_required
@require_http_methods(["GET","POST"])
def sentiment(request):
    result = None
    user_input=""
    
    if request.method == "POST":
        user_input = request.POST.get("text","")
        result = analyze_sentiment(user_input)
        ChatHistory.objects.create(
            user=request.user,
            task="sentiment",
            input_text=user_input,
            result_text=result,
        )

    histories = ChatHistory.objects.filter(
        user=request.user,
        task="sentiment"
    ).order_by("-created_at")[:5]

    context = {
        "tab":"sentiment",
        "result":result,
        "histories": histories,
        "user_input": user_input,
    }
    
    return render(request, "sentiment.html", context)

@require_http_methods(["GET","POST"])
def generate(request):
    result = None
    user_input=""
    
    if request.method == "POST":
        user_input = request.POST.get("text","")
        result = generate_text(user_input)

        if request.user.is_authenticated:
                    ChatHistory.objects.create(
                        user=request.user,
                        task="generate",
                        input_text=user_input,
                        result_text=result,
                    )

    histories = None
    if request.user.is_authenticated:
        histories = ChatHistory.objects.filter(
            user=request.user,
            task="generate"
        ).order_by("-created_at")[:5]

    context = {
        "tab":"generate",
        "result":result,
        "user_input": user_input,
        "histories": histories,
    }
    
    return render(request, "generate.html", context)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get("next")
            return redirect(next_url or "/")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})