from django import forms
from .models import Django_Project
from django.urls import reverse
from django.urls import reverse_lazy

class Form(forms.ModelForm):
    class Meta:
        model=Django_Project
        fields='__all__'


