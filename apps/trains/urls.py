from django.urls import path
from .views import TrainListView, TrainDetailView

app_name = 'trains'
urlpatterns = [
    path('detail/<int:pk>', TrainDetailView.as_view(), name='detail'),
    path('', TrainListView.as_view(), name='home')
]
