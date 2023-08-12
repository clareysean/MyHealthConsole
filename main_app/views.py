import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

# auth
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
#
from .models import Care_provider, Prescription, Photo, User
from .forms import AppointmentForm, UpdateUserForm

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


@login_required
def add_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, user_id=user_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', user_id=user_id)


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
    # care_providers = request.user.care_provider_set.all()
    print(care_providers)
    return render(request, 'care_providers/index.html', {'care_providers': care_providers})


@login_required
def users_detail(request, user_id):
    try:
        care_providers = Care_provider.objects.filter(users=request.user)
    except Care_provider.DoesNotExist:
        care_providers = None

    try:
        prescriptions = Prescription.objects.filter(user=request.user)
    except Prescription.DoesNotExist:
        prescriptions = None

    appointment_form = AppointmentForm()
    return render(request, 'users/detail.html', {
        'care_providers': care_providers,
        'appointment_form': appointment_form,
        'prescriptions': prescriptions,
    })


class PrescriptionCreate(LoginRequiredMixin, CreateView):
    model = Prescription
    fields = ['name', 'description']

    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the cat
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class PrescriptionList(LoginRequiredMixin, ListView):
    model = Prescription


class CareProviderCreate(LoginRequiredMixin, CreateView):
    model = Care_provider
    fields = ['name', 'facility', 'department']

    def form_valid(self, form):
        valid_form = form.save()
        valid_form.users.add(self.request.user)

        return super().form_valid(form)


class CareProviderUpdate(LoginRequiredMixin, UpdateView):
    model = Care_provider
    fields = ['name', 'facility', 'department']


class CareProviderDelete(LoginRequiredMixin, DeleteView):
    model = Care_provider
    success_url = '/'


class UsersDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'user_confirm_delete.html'
    success_url = '/care_providers'


@login_required
def add_appointment(request, user_id):
    # create a ModelForm instance using
    # the data that was submitted in the form
    form = AppointmentForm(request.POST)
    # validate the form
    if form.is_valid():
        # We want a model instance, but
        # we can't save to the db yet
        # because we have not assigned the
        # cat_id FK.
        new_appointment = form.save(commit=False)
        new_appointment.user_id = user_id
        new_appointment.save()
    return redirect('users_detail', user_id=user_id)


@login_required
def unassoc_prescription(request, prescription_id, user_id):
    try:
        prescription = Prescription.objects.get(
            id=prescription_id, user=request.user)
        prescription.delete()
    except Prescription.DoesNotExist:
        pass  # Handle the case where the prescription doesn't exist

    return redirect('users_detail', user_id=user_id)


def update_user(request, user_id):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            # Redirect to the user's profile page
            return redirect('users_detail', user_id=user_id)
    else:
        user_form = UpdateUserForm(instance=request.user, )

    return render(request, 'update_user.html', {'user_form': user_form})
