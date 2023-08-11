from django.shortcuts import render
from .models import Care_provider

# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def care_providers_index(request):
    care_providers = Care_provider.objects.filter(users=request.user)
    return render(request, 'care_providers/index.html', {'care_providers': care_providers})
