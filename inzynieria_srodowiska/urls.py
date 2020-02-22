"""inzynieria_srodowiska URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from water import views

router = routers.DefaultRouter()
router.register(r'water/(?P<station_id>\d+)/valves', views.ValveViewSet, basename='valves')
router.register(r'water/(?P<station_id>\d+)/valve/(?P<valve_id>\d+)', views.ValveViewSet, basename='valve')
router.register(r'water/(?P<station_id>\d+)/valve/(?P<valve_id>\d+)/states', views.ValveStateViewSet,
                basename='valve_states')
router.register(r'water/(?P<station_id>\d+)/containers', views.ContainerViewSet, basename='containers')
router.register(r'water/(?P<station_id>\d+)/container/(?P<container_id>\d+)', views.ContainerViewSet,
                basename='container')
router.register(r'water/(?P<station_id>\d+)/container/(?P<container_id>\d+)/states', views.ContainerStateViewSet,
                basename='container_states')
router.register(r'water/(?P<station_id>\d+)/pumps', views.PumpViewSet, basename='pumps')
router.register(r'water/(?P<station_id>\d+)/pump/(?P<pump_id>\d+)', views.PumpViewSet, basename='pump')
router.register(r'water/(?P<station_id>\d+)/pump/(?P<pump_id>\d+/states)', views.PumpStateViewSet,
                basename='pump_states')

router.register(r'water', views.StationViewSet, basename='stations')

# Wire up our API using automatic URL routing.
# Additionally, we include statesin URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('water/<int:station_id>/stats/', views.receive_water_data),
    path('water/station/steering_states/', views.get_steering_states),
]
