from django.urls import path
from .views import CityListView, CityCreateView, CityDetailView, CityUpdateView, CityDeleteView

app_name = 'cities'
urlpatterns = [
    path('add/', CityCreateView.as_view(), name='add'),
    path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),
    path('', CityListView.as_view(), name='home')

]