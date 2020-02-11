import json

from django.http import HttpResponse
from rest_framework import viewsets

from water.models import ValveState, ContainerState, PumpState, Valve, Container, Pump
from water.serializers import ValveStateSerializer, ContainerStateSerializer, PumpStateSerializer, ValveSerializer, \
    ContainerSerializer


class ValveViewSet(viewsets.ModelViewSet):
    serializer_class = ValveSerializer

    def get_queryset(self):
        return Valve.objects.filter(**self.kwargs).all()

    def create(self, request, *args, **kwargs):
        station_id = self.kwargs['station_id']
        valve_id = self.kwargs['valve_id']

        data = json.loads(request.data)

        # TODO: send command to steering
        return HttpResponse()


class ValveStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ValveStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        valve_id = self.kwargs['valve_id']
        return ValveState.objects.filter(station_state__station_id=station_id, valve__valve_id=valve_id).all()


class ContainerViewSet(viewsets.ModelViewSet):
    serializer_class = ContainerSerializer

    def get_queryset(self):
        return Container.objects.filter(**self.kwargs).all()

    def create(self, request, *args, **kwargs):
        station_id = self.kwargs['station_id']
        container_id = self.kwargs['container_id']

        data = json.loads(request.data)

        # TODO: send command to steering
        return HttpResponse()


class ContainerStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContainerStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        container_id = self.kwargs['container_id']
        return ContainerState.objects.filter(station_state__station_id=station_id,
                                             container__container_id=container_id).all()


class PumpViewSet(viewsets.ModelViewSet):
    serializer_class = ContainerSerializer

    def get_queryset(self):
        return Pump.objects.filter(**self.kwargs).all()

    def create(self, request, *args, **kwargs):
        station_id = self.kwargs['station_id']
        pump_id = self.kwargs['pump_id']

        data = json.loads(request.data)

        # TODO: send command to steering
        return HttpResponse()


class PumpStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PumpStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        pump_id = self.kwargs['pump_id']
        return PumpState.objects.filter(station_state__station_id=station_id, pump__pump_id_=pump_id).all()
