from django.shortcuts import render

# Create your views here.
from apps.cities.models import City


def index(request):
    cities = City.objects.all()
    return render(request, 'cities/index.html', {'cities': cities})