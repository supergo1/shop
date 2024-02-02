from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = User.objects.create_user(
            username=username, password=password, phone=phone, first_name=first_name, last_name=last_name
        )
        login(request, user)
        return redirect('index')
    return render(request, 'sign-up.html')


def personal(request):
    user = request.user
    first_name = request.POST.get('first-name')
    last_name = request.POST.get('last-name')
    phone = request.POST.get('phone')
    user.first_name = first_name
    user.last_name = last_name
    user.phone = phone
    user.save()
    return redirect('profile')


def account_info(request):
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    user = request.user
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    usr = User.objects.filter(username=username)
    if usr:
        messages.error(request, f"""{username} username is taken. Please try again.""")
        print('#################')
        return redirect('profile')
    else:
        user.username = username

    user.email = email
    if password:
        user.set_password(password)
    user.save()
    return redirect('profile')


def profile_view(request):
    if request.method == 'POST':
        action = request.GET.get('action')
        print(action)
        if action == 'personal':
            personal(request)
        elif action == 'account':
            account_info(request)
    return render(request, 'shop-account.html')




