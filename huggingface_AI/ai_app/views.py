from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("AI Home")

def summarize(request):
    return HttpResponse("Summarize Page")

def sentiment(request):
    return HttpResponse("Sentiment Page")

def generate(request):
    return HttpResponse("Generate Page")