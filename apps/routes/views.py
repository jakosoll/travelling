from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView
from .forms import RouteForm, RouteCreateForm, DivErrorList
from .models import Route
from .route import SessionRoute


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None, error_class=DivErrorList)
        if form.is_valid():
            data = form.cleaned_data
            from_city = data['from_city']
            to_city = data['to_city']
            trains = data['trains']
            trains = sorted(trains, key=lambda x: x['total_time'])
            routes = SessionRoute(request)
            routes.clear()  # очищаем сессию перед новым добавлением
            routes.add(trains)

            cities = {'from_city': from_city.name, 'to_city': to_city.name}
            context = {'form': RouteForm(error_class=DivErrorList), 'routes': routes, 'cities': cities}
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})


def save_route(request, route_id):
    if request.method == 'POST':
        form = RouteCreateForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            name = form_data['name']
            route = SessionRoute(request)
            data = route.get_route(route_id)
            route = Route(
                name=name,
                from_city=data['from_city'],
                to_city=data['to_city'],
                travel_time=data['total_time'])
            route.save()
            for train in data['trains']:
                route.across_cities.add(train.id)
            messages.error(request, 'Маршрут сохранен')
            return HttpResponseRedirect('/')
    else:
        route = SessionRoute(request)
        data = route.get_route(route_id)
        if data:
            form = RouteCreateForm()
            context = {'form': form, 'route': data}
            return render(request, 'routes/create.html', context)
        else:
            messages.error(request, 'Невозможно сохранить несуществующий маршрут')
            return HttpResponseRedirect('/')


class RouteDetailView(DetailView):
    queryset = Route.objects.all()
    context_object_name = 'route'
    template_name = 'routes/detail.html'


class RouteListView(ListView):
    queryset = Route.objects.all()
    context_object_name = 'route_list'
    template_name = 'routes/list.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    login_url = '/login/'
    template_name = 'routes/delete.html'
    success_url = reverse_lazy('routes:home')
