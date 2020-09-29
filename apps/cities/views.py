from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from apps.cities.forms import CityForm
from apps.cities.models import City


class CitiesList(ListView):
    model = City
    template_name = 'cities/index.html'
    context_object_name = 'cities'


class CreateCity(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = ''
    success_url = reverse_lazy('cities:home')

