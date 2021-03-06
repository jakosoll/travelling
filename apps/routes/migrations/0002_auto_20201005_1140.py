# Generated by Django 3.1.1 on 2020-10-05 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0001_initial'),
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='from_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_from_city', to='cities.city', verbose_name='Откуда'),
        ),
        migrations.AlterField(
            model_name='route',
            name='to_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_to_city', to='cities.city', verbose_name='Куда'),
        ),
    ]
