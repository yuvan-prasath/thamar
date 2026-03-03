from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('elder', 'Elder'),
        ('volunteer', 'Volunteer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    phone = models.CharField(max_length=20)
    address_line1 = models.TextField()
    address_line2 = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    preferred_language = models.CharField(max_length=50)

    # ✅ ADD THIS
    dob = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Elder(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="elder")
    
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    health_support = models.JSONField(null=True, blank=True)
    communication_mode = models.CharField(max_length=50)
    def __str__(self):
        return f"Elder: {self.profile.user.username}"
class Volunteer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="volunteer")
    skills = models.JSONField(null=True, blank=True)
    availability = models.JSONField(null=True, blank=True)
    experience_level = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    def __str__(self):
        return f"Volunteer: {self.profile.user.username}"
