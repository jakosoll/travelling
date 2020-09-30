from django.db import models

from apps.trains.models import Train


class Route(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    from_city = models.CharField('Откуда', max_length=100)
    to_city = models.CharField('Куда', max_length=100)
    across_cities = models.ManyToManyField(Train, blank=True, verbose_name='Через города')
    travel_time = models.IntegerField('Время в пути')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршурт'
        verbose_name_plural = 'Маршруты'
