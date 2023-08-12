from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

from django.utils import timezone

# now = timezone.now()
# Create your models here.


class Prescription(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('prescription_index')


class Care_provider(models.Model):
    name = models.CharField(max_length=50)
    facility = models.CharField(max_length=75)
    department = models.CharField(max_length=50, default='Family Medicine')

    # Many to many relationship for patients >--< care providers
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('care_provider_detail', kwargs={'care_provider_id': self.id})


class Appointment(models.Model):
    date = models.DateField('Appointment Date')
    time = models.TimeField('Appointment Time')
    location = models.CharField(max_length=75)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Photo(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for user: {self.user.id} @{self.url}"
