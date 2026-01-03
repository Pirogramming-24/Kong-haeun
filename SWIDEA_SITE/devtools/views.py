from django.shortcuts import render, redirect
from .models import Devtool
from .forms import DevtoolForm
from ideas.models import Idea

# Create your views here.
def devtool_list(request):
    devtools = Devtool.objects.all()
    context = {'devtools': devtools}
    return render(request, 'devtools/devtool_list.html', context)

def devtool_create(request):
    if request.method == 'POST':
        form = DevtoolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('devtools:detail', pk=devtool.pk)
    else:
        form = DevtoolForm()
    context = {
        'form': form,
        'mode':'create',
               
    }
    return render(request, 'devtools/devtool_form.html', context)

def devtool_detail(request, pk):
    devtool = Devtool.objects.get(id=pk)
    ideas = Idea.objects.filter(devtool=devtool)
    context = {
        'devtool': devtool,
        'ideas': ideas,
    }
    return render(request, 'devtools/devtool_detail.html', context)

def devtool_update(request, pk):
    devtool = Devtool.objects.get(id=pk)
    if request.method == 'POST':
        form = DevtoolForm(request.POST, instance=devtool)
        if form.is_valid():
            form.save()
            return redirect('devtools:detail', pk=pk)
    else:
        form = DevtoolForm(instance=devtool)

    context = {
        'form': form,
        'mode': 'update',
    }
    return render(request, 'devtools/devtool_form.html', context)

def devtool_delete(request, pk):
    devtool = Devtool.objects.get(id=pk)
    if request.method == 'POST':
        devtool.delete()
    return redirect('devtools:list')
