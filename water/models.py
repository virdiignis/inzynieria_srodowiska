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
