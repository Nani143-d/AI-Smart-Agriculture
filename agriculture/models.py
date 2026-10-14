from django.db import models
from django.contrib.auth.models import User


# ==========================================
# 1. CROP ANALYSIS MODEL
# ==========================================

class CropAnalysis(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    crop_name = models.CharField(max_length=100)
    soil_type = models.CharField(max_length=100)

    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()

    temperature = models.FloatField()
    rainfall = models.FloatField()

    predicted_yield = models.FloatField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crop_name} - {self.created_at:%Y-%m-%d}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Crop Analysis"
        verbose_name_plural = "Crop Analyses"


# ==========================================
# 2. PLANT DISEASE DETECTION MODEL
# ==========================================

class DiseaseDetection(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="crop_images/"
    )

    disease = models.CharField(max_length=200)

    confidence = models.FloatField(
        null=True,
        blank=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disease} ({self.created_at:%Y-%m-%d})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Disease Detection"
        verbose_name_plural = "Disease Detections"


# ==========================================
# 3. LOGIN AND LOGOUT HISTORY MODEL
# ==========================================

class LoginHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="login_history"
    )

    login_time = models.DateTimeField(
        auto_now_add=True
    )

    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

    class Meta:
        ordering = ["-login_time"]
        verbose_name = "Login History"
        verbose_name_plural = "Login History"