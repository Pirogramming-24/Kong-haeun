from django.shortcuts import render

# Create your views here.
def home(request):
    return HttpResponse("AI Home")

def summarize(request):
    result = None

    if request.method == "POST":
        text = request.POST.get("text","").strip()
        if text:
            result = f"{text[:100]}..."

    context = {
        "tab":"summarize",
        "result":result,
    }

    return render(request, "summarize.html", context)

def sentiment(request):
    result = None

    if request.method == "POST":
        text = request.POST.get("text","").strip()
        if text:
            result = "긍정" if "good" in text.lower() else "중립"

    context = {
        "tab":"sentiment",
        "result":result,
    }
    
    return render(request, "sentiment.html", context)

def generate(request):
    result = None

    if request.method == "POST":
        text = request.POST.get("text","").strip()
        if text:
            result = text + "... and this is a generated continuation."

    context = {
        "tab":"generate",
        "result":result,
    }
    
    return render(request, "generate.html", context)