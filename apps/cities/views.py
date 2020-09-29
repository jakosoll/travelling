from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.cities.forms import CityForm
from apps.cities.models import City


def index(request):
    cities = City.objects.all()
    return render(request, 'cities/index.html', {'cities': cities})


class CreateCity(SuccessMessageMixin, CreateView):
    model = City
    form_class = CityForm
    template_name = ''
    success_url = reverse_lazy('city:home')

