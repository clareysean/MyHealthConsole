from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('care_providers/', views.care_providers_index, name='index'),
    path('care_providers/<int:', views.care_providers_index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
]

# TODO: ADD THE REMAINING PATHS, STARTING WITH path('accounts/signup/', views.signup, name='signup'),
