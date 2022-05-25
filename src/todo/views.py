from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import ToDo


def home(request):
    print(request)
    if not request.user.is_authenticated:
        return redirect('register/signin/')

    if request.method == 'POST':
        id = int(request.body.decode("utf-8"),10)
        todo_finished = ToDo.objects.get(id=id, user=request.user)
        todo_finished.finished=True
        todo_finished.save()
        return redirect('')

    todo = ToDo.objects.filter(finished=False, user=request.user)
    return render(request, 'home.html', {'todo': todo})


def create_task(request):
    if not request.user.is_authenticated:
        return redirect('register/signin/')

    if request.method == 'POST':
        user = request.user
        title = request.POST.get("title")
        finish = request.POST.get("finish")
        finish = False if finish is None else True
        description = request.POST.get("description")

        todo = ToDo(user=user, title=title, finished=finish, description=description)
        todo.save()

    return render(request, 'create.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password01 = request.POST.get('password01')
        if password == password01:
            old_user = authenticate(request, username=username, password=password)
            if old_user is None:
                User.objects.create_user(username=username, password=password)
                login(request, user=username)
                return redirect('/')
            else:
                return redirect('/register/signin')

    return render(request, 'register/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/register/signup')

    return render(request, 'register/signin.html')


def signout(request):
    logout(request)
    return redirect('/register/signin')
