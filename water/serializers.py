from django.contrib.auth.models import User
from rest_framework import serializers

from water import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = "__all__"


class StationStateSerializer(serializers.HyperlinkedModelSerializer):
    manual_steering_user = UserSerializer(read_only=True)

    class Meta:
        model = models.StationState
        fields = ("steering_state", "manual_steering_user", "timestamp")


class ValveSerializer(serializers.ModelSerializer):
    station = StationSerializer()

    class Meta:
        model = models.Valve
        fields = "__all__"


class ValveStateSerializer(serializers.ModelSerializer):
    timestamp = serializers.SlugRelatedField(read_only=True, slug_field='timestamp', source='station_state')

    class Meta:
        model = models.ValveState
        fields = ['valve_open', 'timestamp']


class ContainerSerializer(serializers.ModelSerializer):
    station = StationSerializer()

    class Meta:
        model = models.Container
        fields = "__all__"


class ContainerStateSerializer(serializers.ModelSerializer):
    timestamp = serializers.SlugRelatedField(read_only=True, slug_field='timestamp', source='station_state')

    class Meta:
        model = models.ContainerState
        fields = ['container_state', 'timestamp']


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
