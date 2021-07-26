from django.shortcuts import render
from django.http import JsonResponse

from .models import TODO


def home(request):
    return render(request, 'todo.html')

def todo_list(request):
    todos = TODO.objects.all()
    return JsonResponse({'todos': list(todos.values())})

def todo_create(request):
    if request.method == 'POST':
        todo_name = request.POST.get('todo_name')
        todo = TODO.objects.filter(name=todo_name)

        # we need to make sure that this todo does not exist in the database
        if todo.exists():
            return JsonResponse({'status': 'error'})

        todo = TODO.objects.create(name=todo_name)
        return JsonResponse({'todo_name': todo.name, 'status': 'created'})
    
def todo_edit(request):
    if request.method == "POST":
        todo_name = request.POST.get('todo_name')
        # the `new_todo_name` variable will be None in this case
        # because we didn't send it in the AJAX request
        # we still need it in case the user wants to edit the todo's name
        new_todo_name = request.POST.get('new_todo_name')
        completed = request.POST.get('completed')
        edited_todo = TODO.objects.get(name=todo_name)
        
        # if the `completed` variable is not None this means that the user
        # want to mark the todo as complete/incomplete, otherwise the 
        # user want to edit the todo's name
        if completed:
            if completed == '0':
                edited_todo.completed = False
                edited_todo.save()
                return JsonResponse({'status': 'updated'})
            elif completed == '1':
                edited_todo.completed = True
                edited_todo.save()
                return JsonResponse({'status': 'updated'})

        if TODO.objects.filter(name=new_todo_name).exists():
            return JsonResponse({'status': 'error'})

        edited_todo.name = new_todo_name
        edited_todo.save()
        
        context = {
            'new_todo_name': new_todo_name,
            'status': 'updated'
        }
        return JsonResponse(context)
    
def todo_delete(request):
    if request.method == 'POST':
        todo_name = request.POST.get('todo_name')
        TODO.objects.filter(name=todo_name).delete()
        return JsonResponse({'status': "deleted"})   