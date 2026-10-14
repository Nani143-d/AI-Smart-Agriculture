from django import forms
from .models import CropAnalysis, DiseaseDetection

class DiseaseUploadForm(forms.ModelForm):
    class Meta:
        model = DiseaseDetection
        fields = ["image"]
        widgets = {"image": forms.ClearableFileInput(attrs={
            "class": "form-control", "accept": "image/*"
        })}

class FertilizerForm(forms.Form):
    crop = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"e.g. Rice"}))
    nitrogen = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"N value"}))
    phosphorus = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"P value"}))
    potassium = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"K value"}))

class YieldPredictionForm(forms.Form):
    crop = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"e.g. Rice"}))
    soil = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"e.g. Loamy"}))
    nitrogen = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={"class":"form-control","step":"any"}))
    phosphorus = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={"class":"form-control","step":"any"}))
    potassium = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={"class":"form-control","step":"any"}))
    temperature = forms.FloatField(widget=forms.NumberInput(attrs={"class":"form-control","step":"any"}))
    rainfall = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={"class":"form-control","step":"any"}))

class WeatherForm(forms.Form):
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Enter city name"}))

class ChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":3,"placeholder":"Ask about crops, soil, weather..."}))
