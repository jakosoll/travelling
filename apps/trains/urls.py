from django.urls import path
from .views import TrainListView, TrainDetailView, TrainCreateView

app_name = 'trains'
urlpatterns = [
    path('detail/<int:pk>', TrainDetailView.as_view(), name='detail'),
    path('add/', TrainCreateView.as_view(), name='add'),
    path('', TrainListView.as_view(), name='home')
]
