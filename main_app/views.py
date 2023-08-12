import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

# auth
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#
from .models import Care_provider, Prescription, Photo
from .forms import AppointmentForm

# Create your views here.


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def care_provider_detail(request, care_provider_id):
    care_provider = Care_provider.objects.get(id=care_provider_id)
    return render(request, 'care_providers/detail.html', {
        'care_provider': care_provider
    })


@login_required
def care_providers_index(request):
    care_providers = Care_provider.objects.filter(users=request.user)
    return render(request, 'care_providers/index.html', {'care_providers': care_providers})


@login_required
def users_detail(request, user_id):
    care_providers = Care_provider.objects.get(id=user_id)
    appointment_form = AppointmentForm()
    return render(request, 'users/detail.html', {
        'care_providers': care_providers, 'appointment_form': appointment_form
    })


class PrescriptionCreate(LoginRequiredMixin, CreateView):
    model = Prescription
    fields = ['name', 'description']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class CareProviderCreate(LoginRequiredMixin, CreateView):
    model = Care_provider
    fields = ['name', 'facility', 'department']

    def form_valid(self, form):

        form.instance.user = self.request.user

        return super().form_valid(form)
