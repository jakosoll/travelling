from django.urls import path

from .views import index

app_name = 'cities'
urlpatterns = [
    path('', index, name='home')
]