from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import ElderRequest
from accounts.models import Volunteer

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


@staff_member_required
def staff_dashboard(request):

    pending_volunteers = Volunteer.objects.filter(verification_status='Pending')
    total_requests = ElderRequest.objects.count()

    context = {
        'pending_volunteers': pending_volunteers.count(),
        'total_requests': total_requests,
    }

    return render(request, 'staff/dashboard.html', context)

@staff_member_required
def pending_volunteers(request):
    volunteers = Volunteer.objects.filter(verification_status='Pending')

    return render(request, 'staff/pending_volunteers.html', {
        'volunteers': volunteers
    })

@staff_member_required
def approve_volunteer(request, pk):

    volunteer = get_object_or_404(Volunteer, pk=pk)

    volunteer.verification_status = 'approved'
    volunteer.verified_by = request.user
    volunteer.verified_at = timezone.now()
    volunteer.save()

    return redirect('pending_volunteers')

@staff_member_required
def reject_volunteer(request, pk):

    volunteer = get_object_or_404(Volunteer, pk=pk)

    volunteer.verification_status = 'rejected'
    volunteer.verified_by = request.user
    volunteer.verified_at = timezone.now()
    volunteer.save()

    return redirect('pending_volunteers')