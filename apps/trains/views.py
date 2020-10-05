from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import TrainForm
from .models import Train
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class TrainListView(ListView):
    model = Train
    paginate_by = 5
    template_name = 'trains/home.html'
    context_object_name = 'trains'


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'
    context_object_name = 'train'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Train
    form_class = TrainForm
    login_url = '/login/'
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Поезд успешно создан'


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainForm
    login_url = '/login/'
    template_name = 'trains/update.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Поезд успешно отредактирован'


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    login_url = '/login/'
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('trains:home')
