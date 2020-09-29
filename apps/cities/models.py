from django.db import models


class City(models.Model):
    name = models.CharField('Город', unique=True, max_length=70)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name
