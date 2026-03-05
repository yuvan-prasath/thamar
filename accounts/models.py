from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
    ('elder', 'Elder'),
    ('volunteer', 'Volunteer'),
    ('staff', 'Thamar Staff'),
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

    STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

    

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="volunteer")

    skills = models.JSONField(null=True, blank=True)
    availability = models.JSONField(null=True, blank=True)
    experience_level = models.CharField(max_length=50)

    # 🔹 Verification Fields
    id_proof = models.FileField(upload_to='verification_docs/', null=True, blank=True)
 

    verification_status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default='Pending'
)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_volunteers"
    )
    verified_at = models.DateTimeField(null=True, blank=True)

    rating = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if self.verification_status == 'approved' and not self.verified_at:
            self.verified_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Volunteer: {self.profile.user.username}"
    
class ThamarStaff(models.Model):

    DEPARTMENTS = (
        ('verification', 'Verification'),
        ('complaints', 'Complaints'),
        ('operations', 'Operations'),
    )

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="staff"
    )

    department = models.CharField(max_length=100, choices=DEPARTMENTS)
    designation = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Staff: {self.profile.user.username} ({self.department})"