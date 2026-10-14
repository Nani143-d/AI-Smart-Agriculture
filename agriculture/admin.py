from django.contrib import admin
from .models import CropAnalysis, DiseaseDetection, LoginHistory


@admin.register(CropAnalysis)
class CropAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "crop_name",
        "soil_type",
        "predicted_yield",
        "created_at",
    )

    list_filter = ("crop_name", "soil_type", "created_at")
    search_fields = ("crop_name", "soil_type")
    ordering = ("-created_at",)


@admin.register(DiseaseDetection)
class DiseaseDetectionAdmin(admin.ModelAdmin):
    list_display = (
        "disease",
        "confidence",
        "created_at",
    )

    list_filter = ("disease", "created_at")
    search_fields = ("disease", "notes")
    ordering = ("-created_at",)


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "login_time",
        "logout_time",
        "login_status",
    )

    list_filter = ("login_time", "logout_time")

    search_fields = (
        "user__username",
        "user__email",
    )

    readonly_fields = (
        "user",
        "login_time",
        "logout_time",
    )

    ordering = ("-login_time",)

    @admin.display(description="Status")
    def login_status(self, obj):
        if obj.logout_time:
            return "Logged Out"

        return "Logged In"