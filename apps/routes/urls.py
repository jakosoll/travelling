from django.urls import path
from .views import home, find_routes, save_route, RouteListView, RouteDetailView, RouteDeleteView

app_name = 'routes'
urlpatterns = [
    path('find/', find_routes, name='find'),
    path('save_route/', save_route, name='save_route'),
    path('list/', RouteListView.as_view(), name='list'),
    path('detail/<int:pk>', RouteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', RouteDeleteView.as_view(), name='delete'),
    path('', home, name='home')
]