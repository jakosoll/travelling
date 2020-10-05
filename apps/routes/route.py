import copy
from django.conf import settings
from apps.cities.models import City
from apps.trains.models import Train


class SessionRoute:
    def __init__(self, request):
        self.session = request.session
        routes = self.session.get(settings.ROUTE_SESSION_ID)
        if not routes:
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
        self.save()

    def get_route(self, route_id):
        route = copy.deepcopy(self.routes.get(str(route_id)))
        route['from_city'] = City.objects.get(pk=route['from_city'])
        route['to_city'] = City.objects.get(pk=route['to_city'])
        route['trains'] = Train.objects.filter(id__in=route['trains'])
        route['id'] = route_id
        return route

    def __iter__(self):
        routes = copy.deepcopy(self.routes)
        for key, route in routes.items():
            trains_id = [i for i in route['trains']]
            from_city_id = route['from_city']
            to_city_id = route['to_city']
            trains = Train.objects.filter(id__in=trains_id)
            route['id'] = int(key)
            route['trains'] = [train for train in trains]
            route['from_city'] = City.objects.get(pk=from_city_id)
            route['to_city'] = City.objects.get(pk=to_city_id)
            print(route)
            yield route

    def __len__(self):
        return len(self.routes.values())

    def clear(self):
        del self.session[settings.ROUTE_SESSION_ID]
        self.session.modified = True

    def save(self):
        """Сохранение корзины в сессии"""
        self.session[settings.ROUTE_SESSION_ID] = self.routes
        self.session.modified = True
