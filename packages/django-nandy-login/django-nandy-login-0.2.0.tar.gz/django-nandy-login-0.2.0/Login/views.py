from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

from .models import UserProfile
# Create your views here.


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request, exception):
    return render(request, '500.html', status=500)


# Logout view
def logout(request):
    messages.success(request, "Successfully Logged out :)")
    auth.logout(request)
    return redirect('login')


def login(request):
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = auth.authenticate(username=u, password=p)

        if user is not None:
            auth.login(request, user)
            messages.success(request, f'Welcome {u}')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html', {'title': 'Login'})


def register(request):
    if request.method == 'POST':
        employeeId = request.POST['eid']
        uname = request.POST['uname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'email is already taken by others')
                return redirect('register')
            elif User.objects.filter(username=uname):
                messages.error(request, 'Username is taken by others')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=uname, email=email, password=password1)
                userprofile = UserProfile.objects.create(
                    user=user, employeeid=employeeId)
                messages.success(request, 'Registration Success!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords does not match :(')
            return redirect('register')
    elif request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'register.html', {'title': 'Register'})
