from django.urls import path
from .views import home, find_routes

app_name = 'routes'
urlpatterns = [
    path('find/', find_routes, name='find'),
    path('', home, name='home')
]