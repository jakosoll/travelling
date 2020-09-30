from django import forms
from .models import Train
from ..cities.models import City


class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Название',
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'placeholder': ' Введите название поезда'
                               }))
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(
                                           attrs={
                                               'class': 'form-control'
                                           }
                                       ))
    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(
                                         attrs={
                                             'class': 'form-control'
                                         }
                                     ))
    travel_time = forms.CharField(label='Время в пути',
                                  widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control',
                                          'placeholder': ' Введите время в пути'
                                      }))

    class Meta:
        model = Train
        fields = ('name', 'from_city', 'to_city', 'travel_time')
