from django.urls import path
from .views import index

app_name = 'trains'
urlpatterns = [
    path('', index, name='home')
]