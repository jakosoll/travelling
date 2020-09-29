from django.urls import path
from .views import index

app_name = 'routes'
urlpatterns = [
    path('', index, name='home')
]