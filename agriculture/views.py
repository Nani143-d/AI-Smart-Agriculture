import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from agriculture.utils.chatbot import ask_agriculture_ai
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import DiseaseUploadForm, FertilizerForm, YieldPredictionForm, WeatherForm, ChatForm
from .models import CropAnalysis, DiseaseDetection
from .utils.disease_detection import predict_disease
from .utils.yield_prediction import predict_yield
from .utils.fertilizer import recommend_fertilizer
from .utils.weather import get_weather

def home(request):
    return render(request, "home.html")

@login_required
def dashboard(request):
    analyses = CropAnalysis.objects.filter(user=request.user).order_by("-created_at")[:10]
    diseases = DiseaseDetection.objects.filter(user=request.user).order_by("-created_at")[:5]
    return render(request, "dashboard.html", {"analyses": analyses, "diseases": diseases})

@login_required
def disease_detection(request):
    result = None
    form = DiseaseUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        record = form.save(commit=False)
        record.user = request.user
        record.disease = "Analysis pending"
        record.save()
        prediction = predict_disease(record.image.path)
        record.disease = prediction["label"]
        record.confidence = prediction.get("confidence")
        record.notes = prediction["message"]
        record.save()
        result = {"image_url": record.image.url, **prediction}
    return render(request, "disease.html", {"form": form, "result": result})

@login_required
def fertilizer(request):
    form = FertilizerForm(request.POST or None)
    recommendation = None
    if request.method == "POST" and form.is_valid():
        recommendation = recommend_fertilizer(**form.cleaned_data)
    return render(request, "fertilizer.html", {"form": form, "recommendation": recommendation})

@login_required
def yield_prediction(request):
    form = YieldPredictionForm(request.POST or None)
    prediction = None
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        prediction = predict_yield(data)
        CropAnalysis.objects.create(
            user=request.user, crop_name=data["crop"], soil_type=data["soil"],
            nitrogen=data["nitrogen"], phosphorus=data["phosphorus"],
            potassium=data["potassium"], temperature=data["temperature"],
            rainfall=data["rainfall"], predicted_yield=prediction["yield_t_ha"]
        )
    return render(request, "yield_prediction.html", {"form": form, "prediction": prediction})

@login_required
def weather(request):
    form = WeatherForm(request.POST or None)
    weather_data = None
    if request.method == "POST" and form.is_valid():
        weather_data = get_weather(form.cleaned_data["city"])
    return render(request, "weather.html", {"form": form, "weather": weather_data})

# AI Farming Chatbot Page
@login_required
def chatbot(request):
    return render(request, "chatbot.html")


# AI Farming Chatbot API
@login_required
@require_POST
def chatbot_api(request):
    try:
        data = json.loads(request.body)

        question = data.get("message", "").strip()
        history = data.get("history", [])

        if not question:
            return JsonResponse(
                {"error": "Please enter your farming question."},
                status=400,
            )

        if not isinstance(history, list):
            return JsonResponse(
                {"error": "Invalid conversation history."},
                status=400,
            )

        # Keep only the latest 10 conversation entries.
        history = history[-10:]

        answer = ask_agriculture_ai(
            question=question,
            conversation_history=history,
        )

        return JsonResponse({"answer": answer})

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid request data."},
            status=400,
        )

    except Exception:
        # Log the actual exception in your server logs when debugging.
        return JsonResponse(
            {"error": "Unable to process your question right now. Please try again."},
            status=500,
        )
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    error = None
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username",""), password=request.POST.get("password",""))
        if user:
            login(request, user)
            return redirect("dashboard")
        error = "Invalid username or password."
    return render(request, "login.html", {"error": error, "mode": "login"})

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("dashboard")
    return render(request, "login.html", {"form": form, "mode": "register"})

def logout_view(request):
    logout(request)
    return redirect("home")
