from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from apps.cities.forms import CityForm
from apps.cities.models import City


class CityListView(ListView):
    paginate_by = 5
    model = City
    template_name = 'cities/home.html'
    context_object_name = 'cities'


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    form_class = CityForm
    login_url = '/login/'
    template_name = 'cities/create.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Город успешно создан'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = City
    form_class = CityForm
    login_url = '/login/'
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = 'Город успешно отредактирован'
    
    
class CityDeleteView(LoginRequiredMixin, DeleteView):
    model = City
    login_url = '/login/'
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')

