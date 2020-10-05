from django.db import models

from apps.cities.models import City
from apps.trains.models import Train


class Route(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Откуда', related_name='route_from_city')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Куда', related_name='route_to_city')
    across_cities = models.ManyToManyField(Train, blank=True, verbose_name='Через города')
    travel_time = models.IntegerField('Время в пути')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршурт'
        verbose_name_plural = 'Маршруты'
