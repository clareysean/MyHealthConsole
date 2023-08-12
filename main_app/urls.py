from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('care_providers/', views.care_providers_index, name='index'),
    path('care_providers/<int:care_provider_id>/',
         views.care_provider_detail, name='care_provider_detail'),
    path('care_providers/create/', views.CareProviderCreate.as_view(),
         name='care_providers_create'),
    path('accounts/signup/', views.signup, name='signup'),
    path('prescriptions/create/', views.PrescriptionCreate.as_view(),
         name='prescriptions_create'),
    path('users/<int:user_id>/', views.users_detail, name='users_detail'),
]

# TODO: ADD THE REMAINING PATHS, STARTING WITH path('accounts/signup/', views.signup, name='signup'),
