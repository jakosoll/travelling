from django.urls import path
from .views import home

app_name = 'routes'
urlpatterns = [
    path('', home, name='home')
]