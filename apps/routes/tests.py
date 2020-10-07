from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from apps.routes import views as route_views
from apps.routes import graph as gp
from apps.cities import views as cities_views
from apps.routes.forms import RouteForm
from apps.trains.models import Train
from apps.cities.models import City
from apps.routes.route import SessionRoute


class RoutesTestCase(TestCase):

    def setUp(self) -> None:
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')
        t1 = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9)
        t1.save()
        t2 = Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=8)
        t2.save()
        t3 = Train(name='t3', from_city=self.city_A, to_city=self.city_C, travel_time=7)
        t3.save()
        t4 = Train(name='t4', from_city=self.city_C, to_city=self.city_B, travel_time=6)
        t4.save()
        t5 = Train(name='t5', from_city=self.city_B, to_city=self.city_E, travel_time=3)
        t5.save()
        t6 = Train(name='t6', from_city=self.city_B, to_city=self.city_A, travel_time=11)
        t6.save()
        t7 = Train(name='t7', from_city=self.city_A, to_city=self.city_C, travel_time=10)
        t7.save()
        t8 = Train(name='t8', from_city=self.city_E, to_city=self.city_D, travel_time=5)
        t8.save()
        t9 = Train(name='t9', from_city=self.city_D, to_city=self.city_E, travel_time=4)
        t9.save()
        self.graph = gp.get_graph()

    def test_model_city_duplicate(self):
        try:
            a_city = City(name='A')
            a_city.full_clean()
        except ValidationError as e:
            self.assertEqual({'name': ['Город with this Город already exists.']}, e.message_dict)

    def test_model_train_duplicate_name(self):
        try:
            train_2 = Train(name='t2', from_city=self.city_B, to_city=self.city_D, travel_time=7)
            train_2.full_clean()
        except ValidationError as e:
            self.assertEqual({'name': ['Поезд with this Название already exists.']}, e.message_dict)

    def test_train_duplicate_by_cities_and_travel_time(self):
        try:
            train_2 = Train(name='t12', from_city=self.city_B, to_city=self.city_D, travel_time=7)
            train_2.full_clean()
        except ValidationError as e:
            self.assertEqual({'__all__': ['Измените время в пути']}, e.message_dict)

    def test_routes_home_view(self):
        response = self.client.get(reverse('routes:home'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='routes/home.html')
        self.assertEqual(route_views.home, response.resolver_match.func)

    def test_cbv_city_detail(self):
        response = self.client.get(reverse('cities:detail', kwargs={'pk': self.city_A.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='cities/detail.html')
        self.assertEqual(cities_views.CityDetailView.as_view().__name__, response.resolver_match.func.__name__)

    def test_find_all_routes(self):
        all_ways = list(gp.dfs_paths(self.graph, self.city_A.id, self.city_E.id))
        self.assertEqual(len(all_ways), 4)

    def session_route(self):
        self.client.get(reverse('routes:home'))
        route = SessionRoute(self.client)
        all_ways = gp.dfs_paths(self.graph, self.city_A.id, self.city_E.id)
        route.add(gp.dfs_paths(self.graph, self.city_A.id, self.city_E.id))
        routes = [r for r in route]
        self.assertEqual(len(routes), 4)

    def test_form_is_valid(self):
        form_data = {'from_city': self.city_A.id, 'to_city': self.city_E.id,
                     'across_cities': [self.city_C.id], 'travel_time': 30}
        form = RouteForm(form_data)
        self.assertTrue(form.is_valid())

    def test_find_routes_messages_time_error(self):
        response = self.client.post('/find/', {'from_city': self.city_A.id, 'to_city': self.city_E.id,
                                               'across_cities': [self.city_C.id], 'travel_time': 10})
        self.assertContains(response, 'Время в пути больше заданного', 1, 200)

    def test_find_routes_messages_across_cities_error(self):
        response = self.client.post('/find/', {'from_city': self.city_B.id, 'to_city': self.city_E.id,
                                               'across_cities': [self.city_C.id], 'travel_time': 20})
        self.assertContains(response, 'Маршрут, через эти города невозможен', 1, 200)
