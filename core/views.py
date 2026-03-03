from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages 

# Create your views here.
def splash(request):
    return render(request,"splash.html")

def home(request):
    return render(request,"home.html")


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username:", username)
        print("Password:", password)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Login success")
            return redirect("core:home")
        else:
            print("Login failed")
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('core:home')

def elder_request(request):
    return render(request,"elder/elder_request.html")
