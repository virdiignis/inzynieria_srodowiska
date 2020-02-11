from rest_framework import viewsets

from water.models import ValveState, ContainerState, PumpState, StationState
from water.serializers import ValveStateSerializer, ContainerStateSerializer, PumpStateSerializer
import json


class ValveStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ValveStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        valve_id = self.kwargs['valve_id']
        return ValveState.objects.filter(station_state__station_id=station_id, valve__valve_id=valve_id).all()


class ContainerStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContainerStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        container_id = self.kwargs['container_id']
        return ContainerState.objects.filter(station_state__station_id=station_id,
                                             container__container_id=container_id).all()


class PumpStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PumpStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        pump_id = self.kwargs['pump_id']
        return PumpState.objects.filter(station_state__station_id=station_id, pump__pump_id_=pump_id).all()


def receive_water_data(request, station_id):
    if request.method == 'PUT':
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
        pump = request_data.get("pump")

        for x in valves:
            ValveState.objects.create(
                valve_id=x.get("valve_id"),
                valve_state=x.get("valve_state"),
                station_state=station_state
            )

        for x in containers:
            ContainerState.objects.create(
                container_id=x.get("container_id"),
                container_state=x.get("container_state"),
                station_state=station_state
            )

        for x in pump:
            PumpState.objects.create(
                pump_id=x.get("pump_id"),
                pump_state=x.get("pump_state"),
                station_state=station_state
            )
