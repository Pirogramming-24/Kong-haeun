from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from ai_app.services.huggingface import (summarize_text, analyze_sentiment, generate_text)

# Create your views here.
def home(request):
    return HttpResponse("AI Home")

@require_http_methods(["GET","POST"])
def summarize(request):
    result = None

    if request.method == "POST":
        user_input = request.POST.get("text","")
        result = summarize_text(user_input)

    context = {
        "tab":"summarize",
        "result":result,
    }

    return render(request, "summarize.html", context)

@require_http_methods(["GET","POST"])
def sentiment(request):
    result = None

    if request.method == "POST":
        user_input = request.POST.get("text","")
        result = analyze_sentiment(user_input)

    context = {
        "tab":"sentiment",
        "result":result,
    }
    
    return render(request, "sentiment.html", context)

@require_http_methods(["GET","POST"])
def generate(request):
    result = None

    if request.method == "POST":
        user_input = request.POST.get("text","")
        result = generate_text(user_input)

    context = {
        "tab":"generate",
        "result":result,
    }
    
    return render(request, "generate.html", context)