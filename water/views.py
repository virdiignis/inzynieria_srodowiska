import json
from datetime import datetime
from json import JSONDecodeError

from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework import viewsets

from inzynieria_srodowiska import settings
from water.models import Valve, Container, Pump, Station
from water.models import ValveState, ContainerState, PumpState, StationState
from water.serializers import ValveSerializer, \
    ContainerSerializer, PumpSerializer, StationStateSerializer
from water.serializers import ValveStateSerializer, ContainerStateSerializer, PumpStateSerializer, StationSerializer


class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer

    def get_queryset(self):
        return Station.objects.all()


class StationStateViewSet(viewsets.ModelViewSet):
    serializer_class = StationStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        return StationState.objects.filter(station_id=station_id).order_by(
            "-timestamp").all()


class ValveViewSet(viewsets.ModelViewSet):
    serializer_class = ValveSerializer

    def get_queryset(self):
        return Valve.objects.filter(**self.kwargs).all()


class ValveStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ValveStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        valve_id = self.kwargs['valve_id']
        return ValveState.objects.filter(station_state__station_id=station_id, valve__valve_id=valve_id).order_by(
            "-station_state__timestamp", "-id").all()


class ContainerViewSet(viewsets.ModelViewSet):
    serializer_class = ContainerSerializer

    def get_queryset(self):
        return Container.objects.filter(**self.kwargs).all()


class ContainerStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContainerStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        container_id = self.kwargs['container_id']
        return ContainerState.objects.filter(station_state__station_id=station_id,
                                             container__container_id=container_id).order_by(
            "-station_state__timestamp", "-id").all()


class PumpViewSet(viewsets.ModelViewSet):
    serializer_class = PumpSerializer

    def get_queryset(self):
        return Pump.objects.filter(**self.kwargs).all()


class PumpStateViewSet(viewsets.ModelViewSet):
    serializer_class = PumpStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        pump_id = self.kwargs['pump_id']
        return PumpState.objects.filter(station_state__station_id=station_id, pump__pump_id=pump_id).order_by(
            "-station_state__timestamp", "-id").all()


def receive_water_data(request, station_id):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
        except JSONDecodeError:
            return HttpResponseBadRequest("Improperly formatted json")

        steering_state = request_data.get("steering_state", None)
        timestamp = float(request_data.get("timestamp"))

        if steering_state is None:
            steering_state = StationState.objects.filter(station_id=station_id).latest("timestamp").steering_state

        station_state = StationState.objects.create(
            station_id=station_id,
            timestamp=datetime.fromtimestamp(timestamp),
            steering_state=steering_state
        )

        valves = request_data["valves"]
        containers = request_data["containers"]
        pumps = request_data["pumps"]

        ValveState.objects.bulk_create(
            ValveState(
                valve=Valve.objects.get(station_id=station_id, valve_id=valve["valve_id"]),
                valve_open=valve["valve_open"],
                station_state=station_state
            ) for valve in valves
        )

        ContainerState.objects.bulk_create(
            ContainerState(
                container=Container.objects.get(station_id=station_id, container_id=container["container_id"]),
                container_state=container["container_state"],
                station_state=station_state
            ) for container in containers
        )

        PumpState.objects.bulk_create(
            PumpState(
                pump=Pump.objects.get(station_id=station_id, pump_id=pump["pump_id"]),
                pump_state=pump["pump_state"],
                station_state=station_state
            ) for pump in pumps
        )

        return HttpResponse()


def get_steering_states(request):
    if request.method == 'GET':
        return JsonResponse(dict(settings.steering_states))
