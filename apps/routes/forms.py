from django import forms
from django.forms.utils import ErrorList

from apps.cities.models import City
from .graph import get_graph, dfs_paths

from .models import Route
from ..trains.models import Train


class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control js-example-basic-single'}))
    across_cities = forms.ModelMultipleChoiceField(label='Через города', queryset=City.objects.all(), required=False,
                                                   widget=forms.SelectMultiple(
                                                       attrs={'class': 'form-control js-example-basic-multiple'}))
    travel_time = forms.CharField(label='Время в пути',
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control',
                                             'placeholder': ' Введите время в пути'
                                             }))

    def clean(self, *args, **kwargs):
        from_city = self.cleaned_data.get('from_city')
        to_city = self.cleaned_data.get('to_city')
        across_cities_data = self.cleaned_data.get('across_cities')
        travel_time = self.cleaned_data.get('travel_time')
        graph = get_graph()
        all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
        if len(all_ways) == 0:
            raise forms.ValidationError('Маршрута, удовлетворяющего условиям не существует.')
        if across_cities_data:
            across_cities = [city.id for city in across_cities_data]  # получаем id промежуточных точек
            right_ways = []
            for way in all_ways:  # проходимся циклом по всем маршрутам и проверяем промежуточные точки
                if all(point in way for point in across_cities):  # если все точки в маршруте, добавляем в список
                    right_ways.append(way)
            if not right_ways:  # если нет ни одного маршрута с такими точками, возвращаем ошибку
                raise forms.ValidationError('Маршрут через эти города невозможен')
        else:
            right_ways = all_ways

        trains = []
        for route in right_ways:
            tmp = {'trains': []}
            total_time = 0
            for i in range(len(route) - 1):
                qs = Train.objects.filter(from_city=route[i], to_city=route[i + 1])
                qs = qs.order_by('travel_time').first()
                total_time += qs.travel_time
                tmp['trains'].append(qs)
            tmp['total_time'] = total_time
            if total_time <= int(travel_time):
                tmp['from_city'] = from_city
                tmp['to_city'] = to_city
                trains.append(tmp)
        if not trains:
            raise forms.ValidationError('Время в пути больше заданного')
        self.cleaned_data['trains'] = trains
        return super(RouteForm, self).clean()


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="alert alert-secondary" role="alert">' \
               '<h5 class="text-center">Не удалось ничего найти:</h5>%s</div>' % ''.join(
            ['<p class="text-center">%s<p>' % e for e in self])


class RouteCreateForm(forms.ModelForm):
    name = forms.CharField(label='Назовите маршрут', widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))

    class Meta:
        model = Route
        fields = ['name']
