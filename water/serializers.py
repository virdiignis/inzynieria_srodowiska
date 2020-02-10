from rest_framework import serializers

from water import models


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = "__all__"


class ValveSerializer(serializers.ModelSerializer):
    station = StationSerializer()

    class Meta:
        model = models.Valve
        fields = "__all__"


class ValveStateSerializer(serializers.ModelSerializer):
    valve = ValveSerializer()
    station_state = serializers.SlugRelatedField(read_only=True, slug_field='timestamp')

    class Meta:
        model = models.ValveState
        fields = ['valve_state', 'station_state']
