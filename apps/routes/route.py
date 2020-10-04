from typing import List, Dict, Union
import copy
from django.conf import settings
from django.forms.models import model_to_dict
from apps.cities.models import City
from apps.trains.models import Train


class SessionRoute:
    def __init__(self, request):
        self.session = request.session
        routes = self.session[settings.ROUTE_SESSION_ID] = {}
        self.routes = routes
        self.count = 0

    def add(self, routes):

        for route in routes:
            self.count += 1
            trains_id = []
            for train in route['trains']:
                trains_id.append(str(train.id))
            self.routes[str(self.count)] = {
                'from_city': str(route['from_city'].id),
                'to_city': str(route['to_city'].id),
                'trains': trains_id,
                'total_time': route['total_time']
            }
        print(self.routes)
        self.save()

    def sorted(self):
        self.routes = sorted(self.routes, key=lambda x: x['total_time'])

    def __iter__(self):
        routes = copy.deepcopy(self.routes)
        for route in routes.values():
            trains_id = [i for i in route['trains']]
            from_city_id = route['from_city']
            to_city_id = route['to_city']
            trains = Train.objects.filter(id__in=trains_id)
            route['trains'] = [train for train in trains]
            route['from_city'] = City.objects.get(pk=from_city_id)
            route['to_city'] = City.objects.get(pk=to_city_id)
            print(route)
            yield route

    def __len__(self):
        return len(self.routes.values())

    def save(self):
        """Сохранение корзины в сессии"""
        self.session[settings.ROUTE_SESSION_ID] = self.routes
        self.session.modified = True
