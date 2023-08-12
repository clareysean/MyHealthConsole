from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('care_providers/', views.care_providers_index, name='index'),
    path('care_providers/<int:care_provider_id>/',
         views.care_provider_detail, name='care_provider_detail'),
    path('care_providers/<int:pk>/update/',
         views.CareProviderUpdate.as_view(), name='care_provider_update'),
    path('care_providers/create/', views.CareProviderCreate.as_view(),
         name='care_providers_create'),
    path('care_provider/<int:pk>/delete/',
         views.CareProviderDelete.as_view(), name='care_provider_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('prescriptions/create/', views.PrescriptionCreate.as_view(),
         name='prescriptions_create'),
    path('prescriptions/', views.PrescriptionList.as_view(),
         name='prescription_index'),
    path('users/<int:prescription_id>/unassoc_prescription/<int:user_id>/',
         views.unassoc_prescription, name='unassoc_prescription'),
    path('users/<int:user_id>/', views.users_detail, name='users_detail'),
    path('users/<int:user_id>/update/',
         views.update_user, name='users_update'),
    path('users/<int:pk>/delete/', views.UsersDelete.as_view(), name='users_delete'),
    path('users/<int:user_id>/add_photo/', views.add_photo, name='add_photo'),
    path('users/<int:user_id>/add_appointment/',
         views.add_appointment, name='add_appointment'),


]

# TODO: ADD THE REMAINING PATHS, STARTING WITH path('accounts/signup/', views.signup, name='signup'),
