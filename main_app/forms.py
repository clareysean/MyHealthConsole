from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Appointment
from django.contrib.auth.forms import UserChangeForm


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
