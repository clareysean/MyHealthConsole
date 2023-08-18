from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Appointment
from django.contrib.auth.forms import UserChangeForm
from django import forms


class AppointmentForm(ModelForm):
    def clean_care_provider(self):
        care_provider = self.cleaned_data['care_provider']
        if care_provider is None or care_provider.name == "---------":
            raise forms.ValidationError("Please select a valid care provider.")
        return care_provider

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'location',
                  'purpose', 'care_provider']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
