from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from .forms import RouteForm, RouteCreateForm
from .models import Route
from ..trains.models import Train
from typing import List


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
       из одного города в другой. Вариант посещения
       одного и того же города более одного раза,
        не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph():
    qs = Train.objects.values()
    from_city_set = set(i['from_city_id'] for i in qs)
    graph = {}
    for city in from_city_set:
        trains = Train.objects.filter(from_city=city).values('to_city')
        tmp = set(i['to_city'] for i in trains)
        graph[city] = tmp
    return graph


def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


def find_routes(request):
    if request.method == "POST":
        form = RouteForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data  # получаем данные из формы
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities_form = data['across_cities']
            travel_time = data['travel_time']  # раскладываем данные в переменные
            graph = get_graph()  # получаем граф маршрутов
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))  # получаем список всех маршрутов
            if len(all_ways) == 0:
                messages.error(request, 'Маршрута, удовлетворяющего условиям не существует.')
                return render(request, 'routes/home.html', {'form': form})
            if across_cities_form:
                across_cities = [city.id for city in across_cities_form]  # получаем id промежуточных точек
                right_ways = []
                for way in all_ways:  # проходимся циклом по всем маршрутам и проверяем промежуточные точки
                    if all(point in way for point in across_cities):  # если все точки в маршруте, добавляем в список
                        right_ways.append(way)
                if not right_ways:  # если нет ни одного маршрута с такими точками, возвращаем ошибку
                    messages.error(request, 'Маршрут, через эти города невозможен')
                    return render(request, 'routes/home.html', {'form': form})
            else:
                right_ways = all_ways

            trains = []
            for route in right_ways:
                tmp = {'trains': []}
                total_time = 0
                for i in range(len(route)-1):
                    qs = Train.objects.filter(from_city=route[i], to_city=route[i+1])
                    qs = qs.order_by('travel_time').first()
                    total_time += qs.travel_time
                    tmp['trains'].append(qs)
                tmp['total_time'] = total_time
                if total_time <= int(travel_time):
                    trains.append(tmp)
            if not trains:
                messages.error(request, 'Время в пути больше заданного')
                return render(request, 'routes/home.html', {'form': form})

            routes = []
            cities = {'from_city': from_city.name, 'to_city': to_city.name}  # города, будем рендерить в шаблоне
            for train in trains:
                routes.append({
                    'route': train['trains'],
                    'total_time': train['total_time'],
                    'from_city': from_city.name,
                    'to_city': to_city.name
                })
            sorted_routes = sorted(routes, key=lambda x: x['total_time'])
            context = {'form': RouteForm(), 'routes': sorted_routes, 'cities': cities}
            return render(request, 'routes/home.html', context)
        return render(request, 'routes/home.html', {'form': form})
    else:
        messages.error(request, 'Создайте маршрут')
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})


def save_route(request):
    if request.method == 'POST':
        form = RouteCreateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            total_time = data['travel_time']
            from_city: str = data['from_city']
            to_city: str = data['to_city']
            across_cities: List[str] = data['across_cities'].split()
            trains_id = [int(i) for i in across_cities if i.isalnum()]
            qs = Train.objects.filter(id__in=trains_id)
            route = Route(name=name, from_city=from_city, to_city=to_city, travel_time=total_time)
            route.save()
            for tr in qs:
                route.across_cities.add(tr.id)
            messages.error(request, 'Маршрут сохранен')
            return HttpResponseRedirect('/')
        else:
            assert False
    else:
        data = request.GET
        if data:
            total_time = data['total_time']
            from_city: str = data['from_city']
            to_city: str = data['to_city']
            across_cities: List[str] = data['across_cities'].split()
            trains_id = [int(i) for i in across_cities if i.isalnum()]
            qs = Train.objects.filter(id__in=trains_id)
            train_list = ' '.join(str(i) for i in trains_id)
            form = RouteCreateForm(initial={'from_city': from_city,
                                            'to_city': to_city,
                                            'travel_time': total_time,
                                            'across_cities': train_list
                                            })
            route_desc = []
            for train in qs:
                desc = f'Поезд № {train.name} следующий из г. {train.from_city} в г. {train.to_city}. ' \
                        f'Время в пути {train.travel_time} ч.'
                route_desc.append(desc)
            context = {'form': form,
                       'route_desc': route_desc,
                       'from_city': from_city,
                       'to_city': to_city,
                       'total_time': total_time}
            return render(request, 'routes/create.html', context)
        else:
            messages.error(request, 'Невозможно сохранить несуществующий маршрут')
            return HttpResponseRedirect('/')
