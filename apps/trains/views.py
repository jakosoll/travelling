from .models import Train
from django.views.generic import ListView, DetailView


class TrainListView(ListView):
    model = Train
    paginate_by = 5
    template_name = 'trains/home.html'
    context_object_name = 'trains'


class TrainDetailView(DetailView):
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'
