from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator

from .forms import TaskForm
from .models import Task
# Create your views here.
@login_required
def taskList(request):
    search = request.GET.get('search')
    filterStatus = request.GET.get('filter')
    if search:
        tasks = Task.objects.filter(title__icontains=search, user=request.user)
    
    elif filterStatus:
        tasks = Task.objects.filter(done=filterStatus, user=request.user)
    
    else:    
        tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user)
        paginator = Paginator(tasks_list, 3)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    return render(request, 'tasks/list.html', {'tasks': tasks})

@login_required
def taskView(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    return render(request, 'tasks/task.html', {'task': task})

@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.user = request.user
            task.save()
            messages.info(request, 'Item salvo com sucesso')
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form': form})

@login_required
def editTask(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.done = 'Doing'
            task.save()
            messages.info(request, 'Item atualizado com sucesso')
            return redirect('/')
        else:
            messages.error(request, 'Erro de validação')
            return render(request, 'tasks/edittask.html', {'form':form, 'task': task})
    else:
        return render(request, 'tasks/edittask.html', {'form':form, 'task': task})

@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    task.delete()
    messages.warning(request, 'Item removido com sucesso')
    return redirect('/')

@login_required
def doneTask(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    task.done = 'done'
    task.save()
    messages.success(request, 'Tarefa finalizada')
    return redirect('/')