from django.db import models
from apps.cities.models import City
from django.core.exceptions import ValidationError


class Train(models.Model):
    name = models.CharField('Название', max_length=80, unique=True)
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Откуда', related_name='from_city')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Куда', related_name='to_city')
    travel_time = models.IntegerField('Время в пути')

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поезда'
        ordering = ['travel_time']

    def __str__(self):
        return f'Поезд № {self.name} из {self.from_city} в {self.to_city}'

    def clean(self, *args, **kwargs):
        if self.from_city == self.to_city:
            raise ValidationError('Измените город прибытия на другой')
        qs = Train.objects.filter(from_city=self.from_city,
                                  to_city=self.to_city, travel_time=self.travel_time).exclude(pk=self.pk)
        if qs:
            raise ValidationError('Измените время в пути')
        return super(Train, self).clean()

