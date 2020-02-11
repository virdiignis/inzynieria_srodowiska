from rest_framework import viewsets

from water.models import ValveState, ContainerState, PumpState
from water.serializers import ValveStateSerializer, ContainerStateSerializer, PumpStateSerializer


class ValveStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ValveStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        valve_id = self.kwargs['valve_id']
        ValveState.objects.filter(station_state__station_id=station_id, valve__valve_id=valve_id).all()


class ContainerStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContainerStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        container_id = self.kwargs['container_id']
        ContainerState.objects.filter(station_state__station_id=station_id, container__container_id=container_id).all()


class PumpStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PumpStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        pump_id = self.kwargs['pump_id']
        PumpState.objects.filter(station_state__station_id=station_id, pump__pump_id_=pump_id).all()


