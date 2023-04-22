from django.shortcuts import render, redirect
from .models import MyUser
import random
# Create your views here.

user_list = []
message = ''
count = 0
login_user = ''

def home(request):
    return render(request, 'main/home.html', context={
        'login_user':login_user
    })

def login(request):
    global message, count, user_list, login_user
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user_ = MyUser.objects.all()
        for i in user_:
            if name == i.name and password == i.password:
                login_user = name
                return redirect('home')
        else:
            message = 'No user Enter valid user'
            user_list.append(name)
            if user_list.count(name) == 3:
                count = 3
                return redirect('error')
            else:
                return redirect('login')
    return render(request, 'main/login.html', context={
        'message':message,
        
    })


def register(request):
    global message
    char = '!@#$%^&*'
    char_count = 0
    number_count = 0
    let_count = 0
    if request.method == 'POST':
        name = request.POST.get('name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        for i in MyUser.objects.all():
            if name == i.name:
                message = 'Name in DB ERROR'
                return redirect('register')
        else:
            if password1 != password2:
                message = 'Password1 != Password2'
                return redirect('register')
            else:
                if len(password1) < 8:
                    message = 'Enter len > 8 !!!'
                    return redirect('register')
                else:
                    for i in password1:
                        if i.isdigit():
                            number_count += 1
                        elif i in char:
                            char_count += 1
                        else:
                            let_count += 1
                    if number_count >= 1 and char_count >= 1 and let_count >= 6:
                        MyUser.objects.create(name=name, password=password1)
                        return redirect('home')
                    else:
                        message = 'Char Number Letter Error'
                        return redirect('register')
    return render(request, 'main/signup.html', context={
        'message':message
    })
    
random_text = ['AHGS7A456', 'A1B2C3', 'h!sgj!SA45', 'AAB748!#Rda']
random_capcha = random.choice(random_text)

def error(request):
    global count, message, user_list, random_capcha, random_text
    if request.method == 'POST':
        capcha = request.POST.get('capcha')
        if capcha == random_capcha:
            count = 0
            user_list = []
            return redirect('login')
        else:
            message = 'Enter valid capcha'
            random_capcha = random.choice(random_text)
            return redirect('error')
    return render(request, 'main/error.html', context={
        'random_capcha':random_capcha,
        'message':message,
        'count':count,
        'user_list':user_list
    })

def logout(request):
    global login_user
    login_user = ''
    return redirect('home')