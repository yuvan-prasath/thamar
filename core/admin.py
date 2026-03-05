from django.contrib import admin
from .models import ElderRequest


@admin.register(ElderRequest)
class ElderRequestAdmin(admin.ModelAdmin):

    # -------------------------
    # LIST PAGE CONFIGURATION
    # -------------------------
    list_display = (
        "id",
        "elder",
        "volunteer",
        "purpose",
        "status",
        "risk_level",
        "emergency_visits",
        "created_at",
    )

    list_filter = (
        "status",
        "purpose",
        "risk_level",
        "chronic_disease",
        "mobility_issue",
        "recent_fall",
        "created_at",
    )

    search_fields = (
        "elder__username",
        "elder__email",
        "volunteer__username",
        "volunteer__email",
    )

    ordering = ("-created_at",)

    list_editable = (
        "status",
        "volunteer",
    )

    # -------------------------
    # DETAIL PAGE CONFIGURATION
    # -------------------------
    readonly_fields = (
        "risk_score",
        "risk_level",
        "created_at",
        "updated_at",
    )

    fieldsets = (

        ("Elder Information", {
            "fields": (
                "elder",
            
            )
        }),

        ("Request Details", {
            "fields": (
                "purpose",
                "purpose_description",
            )
        }),

        ("Health Indicators", {
            "fields": (
                "chronic_disease",
                "mobility_issue",
                "recent_fall",
                "emergency_visits",
            )
        }),

        ("Assignment & Status", {
            "fields": (
                "status",
                "volunteer",
            )
        }),

        ("Risk Assessment", {
            "fields": (
                "risk_score",
                "risk_level",
            )
        }),

        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    # -------------------------
    # PERFORMANCE OPTIMIZATION
    # -------------------------
    list_select_related = ("elder", "volunteer")