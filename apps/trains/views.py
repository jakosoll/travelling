from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import TrainForm
from .models import Train
from django.views.generic import ListView, DetailView, CreateView


class TrainListView(ListView):
    model = Train
    paginate_by = 5
    template_name = 'trains/home.html'
    context_object_name = 'trains'


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create.html'
    success_url = reverse_lazy('trains:home')
    success_message = 'Поезд успешно создан'
