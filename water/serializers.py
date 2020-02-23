from rest_framework import serializers

from water import models


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = "__all__"


class StationStateSerializer(serializers.ModelSerializer):
    station = StationSerializer()

    class Meta:
        model = models.StationState
        fields = "__all__"


class ValveSerializer(serializers.ModelSerializer):
    station = StationSerializer()

    class Meta:
        model = models.Valve
        fields = "__all__"


class ValveStateSerializer(serializers.ModelSerializer):
    valve = ValveSerializer()
    timestamp = serializers.SlugRelatedField(read_only=True, slug_field='timestamp', source='station_state')

    class Meta:
        model = models.ValveState
        fields = ['valve_open', 'valve', 'timestamp']


class ContainerSerializer(serializers.ModelSerializer):
    station = StationSerializer()

    class Meta:
        model = models.Container
        fields = "__all__"


class ContainerStateSerializer(serializers.ModelSerializer):
    container = ContainerSerializer()
    timestamp = serializers.SlugRelatedField(read_only=True, slug_field='timestamp', source='station_state')

    class Meta:
        model = models.ContainerState
        fields = ['container_state', 'container', 'timestamp']


class PumpSerializer(serializers.ModelSerializer):
    station = StationSerializer()

    class Meta:
        model = models.Pump
        fields = "__all__"


class PumpStateSerializer(serializers.ModelSerializer):
    timestamp = serializers.SlugRelatedField(read_only=True, slug_field='timestamp', source='station_state')

    class Meta:
        model = models.PumpState
        fields = ['pump_state', 'timestamp']
