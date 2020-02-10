from rest_framework import viewsets

from water.models import ValveState
from water.serializers import ValveStateSerializer


class ValveStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ValveStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        valve_id = self.kwargs['valve_id']
        ValveState.objects.filter(station_state__station_id=station_id, valve_id=valve_id).all()
