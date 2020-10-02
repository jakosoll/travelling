from django.urls import path
from .views import home, find_routes, save_route

app_name = 'routes'
urlpatterns = [
    path('find/', find_routes, name='find'),
    path('save_route/', save_route, name='save_route'),
    path('', home, name='home')
]