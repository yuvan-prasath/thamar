from django.db import models
from django.conf import settings



class ElderRequest(models.Model):

    PURPOSE_CHOICES = [
        ("medical", "Medical Assistance"),
        ("emergency", "Emergency Help"),
        ("daily", "Daily Living Support"),
        ("mobility", "Mobility Support"),
        ("other", "Other"),
    ]

    YES_NO_CHOICES = [
        (1, "Yes"),
        (0, "No"),
    ]
    STATUS_CHOICES = [
    ("pending", "Pending"),
    ("assigned", "Volunteer Assigned"),
    ("completed", "Completed"),
]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    elder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="elder_requests"
    )
    volunteer = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="assigned_requests"
    )

    age = models.PositiveIntegerField()

    purpose = models.CharField(
        max_length=20,
        choices=PURPOSE_CHOICES
    )

    purpose_description = models.TextField(
        blank=True,
        null=True
    )

    chronic_disease = models.IntegerField(
        choices=YES_NO_CHOICES
    )

    mobility_issue = models.IntegerField(
        choices=YES_NO_CHOICES
    )

    recent_fall = models.IntegerField(
        choices=YES_NO_CHOICES
    )

    emergency_visits = models.PositiveIntegerField(
        default=0
    )

    risk_score = models.FloatField(
        blank=True,
        null=True
    )

    risk_level = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.elder.username} - {self.purpose} - {self.created_at}"
