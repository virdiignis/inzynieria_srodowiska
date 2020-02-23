import json

from django.http import HttpResponse
from rest_framework import viewsets

from inzynieria_srodowiska import settings
from water.models import Valve, Container, Pump, Station
from water.models import ValveState, ContainerState, PumpState, StationState
from water.serializers import ValveSerializer, \
    ContainerSerializer, PumpSerializer
from water.serializers import ValveStateSerializer, ContainerStateSerializer, PumpStateSerializer, StationSerializer


class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer

    def get_queryset(self):
        return Station.objects.all()


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
    serializer_class = PumpSerializer

    def get_queryset(self):
        return Pump.objects.filter(**self.kwargs).all()

    def create(self, request, *args, **kwargs):
        station_id = self.kwargs['station_id']
        pump_id = self.kwargs['pump_id']

        data = json.loads(request.data)

        # TODO: send command to steering
        return HttpResponse()


class PumpStateViewSet(viewsets.ModelViewSet):
    serializer_class = PumpStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        pump_id = self.kwargs['pump_id']
        return PumpState.objects.filter(station_state__station_id=station_id, pump__pump_id=pump_id).all()


def receive_water_data(request, station_id):
    if request.method == 'POST':
        # TODO: try/except

        request_data = json.loads(request.body)

        steering_state = request_data.get("steering_state", None)
        timestamp = request_data.get("timestamp")

        if steering_state is None:
            steering_state = StationState.objects.filter(station_id=station_id).order_by(
                "timestamp").last().steering_state

        station_state = StationState.objects.create(
            station_id=station_id,
            timestamp=timestamp,
            steering_state=steering_state
        )

        valves = request_data.get("valves")
        containers = request_data.get("containers")
        pumps = request_data.get("pumps")

        for valve in valves:
            ValveState.objects.create(
                valve_id=valve.get("valve_id"),
                valve_open=valve.get("valve_open"),
                station_state=station_state
            )

        for container in containers:
            ContainerState.objects.create(
                container_id=container.get("container_id"),
                container_state=container.get("container_state"),
                station_state=station_state
            )

        for pump in pumps:
            PumpState.objects.create(
                pump_id=pump.get("pump_id"),
                pump_state=pump.get("pump_state"),
                station_state=station_state
            )

        return HttpResponse()


def get_steering_states(request):
    if request.method == 'GET':
        print(json.dumps(dict(settings.steering_states)))
        return HttpResponse(json.dumps(dict(settings.steering_states)),
                            content_type='application/javascript; charset=utf8')
