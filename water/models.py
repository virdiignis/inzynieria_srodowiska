from django.contrib.auth.models import User
from django.db import models


class Station(models.Model):
    descriptive_location = models.TextField()


class StationState(models.Model):
    steering_states = (
        ("AU", "Automatic"),
        ("RM", "Remote Manual"),
        ("LM", "Local Manual"),
        ("OF", "OFF"),
    )
    steering_state = models.CharField(max_length=2, choices=steering_states, default="AU")

    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    manual_steering_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    timestamp = models.TimeField()


class Container(models.Model):
    station = models.ForeignKey(Station, related_name="containers", on_delete=models.CASCADE)
    container_id = models.PositiveIntegerField()
    # MAX MIN ?


# LOG
class ContainerState(models.Model):
    container = models.ForeignKey(Container, related_name="container", on_delete=models.CASCADE)
    container_state = models.PositiveIntegerField()
    station_state = models.ForeignKey(StationState, related_name="containers", on_delete=models.CASCADE)


class Valve(models.Model):
    station = models.ForeignKey(Station, related_name="valves", on_delete=models.CASCADE)
    valve_id = models.PositiveIntegerField()


class ValveState(models.Model):
    valve = models.ForeignKey(Valve, related_name="valves", on_delete=models.CASCADE)
    valve_state = models.BooleanField()
    station_state = models.ForeignKey(StationState, related_name="valves", on_delete=models.CASCADE)


class Pump(models.Model):
    station = models.ForeignKey(Station, related_name="pumps", on_delete=models.CASCADE)
    valve_id = models.PositiveIntegerField()


class PumpState(models.Model):
    valve = models.ForeignKey(Pump, related_name="pumps", on_delete=models.CASCADE)
    valve_state = models.BooleanField()
    station_state = models.ForeignKey(StationState, related_name="pumps", on_delete=models.CASCADE)
