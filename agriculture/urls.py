from django.urls import path
from . import views

urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # AI Crop Disease Detection
    path("disease/", views.disease_detection, name="disease"),

    # Fertilizer Recommendation
    path("fertilizer/", views.fertilizer, name="fertilizer"),

    # Crop Yield Prediction
    path("yield-prediction/", views.yield_prediction, name="yield_prediction"),

    # Weather Information
    path("weather/", views.weather, name="weather"),

    # AI Farming Chatbot
    path("chatbot/", views.chatbot, name="chatbot"),

    # AI Chatbot API
    path("chatbot/ask/", views.chatbot_api, name="chatbot_api"),

    # User Authentication
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
]