from django.urls import path
from .views import index
from .views import CitiesList

app_name = 'cities'
urlpatterns = [
    path('', CitiesList.as_view(), name='home')
]