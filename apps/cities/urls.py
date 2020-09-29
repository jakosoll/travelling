from django.urls import path
from .views import index

app_name = 'city'
urlpatterns = [
    path('', index, name='home')
]