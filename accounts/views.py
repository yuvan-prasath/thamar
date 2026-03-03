from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime

from .models import Profile, Elder, Volunteer


def register(request):
    if request.method == "POST":
        role = request.POST.get("role")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        full_name = request.POST.get("full_name")
        dob_raw = request.POST.get("dob")  # ✅ NEW

        # Check username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("accounts:register")

        # Split name
        name_parts = full_name.strip().split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Parse DOB safely
        dob = None
        if dob_raw:
            try:
                dob = datetime.strptime(dob_raw, "%Y-%m-%d").date()
            except ValueError:
                dob = None

        # Create Profile (DOB stored here)
        profile = Profile.objects.create(
            user=user,
            role=role,
            phone=request.POST.get("phone"),
            address_line1=request.POST.get("address_line1"),
            address_line2=request.POST.get("address_line2"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            pincode=request.POST.get("pincode"),
            preferred_language=request.POST.get("preferred_language"),
            dob=dob,  # ✅ SAVED HERE
        )

        # Role-specific models
        if role == "elder":
            Elder.objects.create(
                profile=profile,
                emergency_contact_name=request.POST.get("emergency_contact_name"),
                emergency_contact_phone=request.POST.get("emergency_contact_phone"),
                health_support=request.POST.getlist("health_support"),  # JSONField
                communication_mode=request.POST.get("communication_mode"),
            )

        elif role == "volunteer":
            Volunteer.objects.create(
                profile=profile,
                skills=request.POST.getlist("skills"),          # JSONField
                availability=request.POST.getlist("availability"),  # JSONField
                experience_level=request.POST.get("experience_level"),
            )

        messages.success(request, "Registration successful!")
        return redirect("core:login")

    return render(request, "register.html")