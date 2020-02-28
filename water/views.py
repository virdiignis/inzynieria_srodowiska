import json
from json import JSONDecodeError

import requests
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from inzynieria_srodowiska import settings
from water.filters import DatetimeRangeFilterBackend
from water.models import Valve, Container, Pump, Station, Order, SteeringUser
from water.models import ValveState, ContainerState, PumpState, StationState
from water.serializers import ValveSerializer, \
    ContainerSerializer, PumpSerializer, StationStateSerializer, UserSerializer
from water.serializers import ValveStateSerializer, ContainerStateSerializer, PumpStateSerializer, StationSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class StationViewSet(viewsets.ModelViewSet):
    serializer_class = StationSerializer

    def get_queryset(self):
        return Station.objects.all()


class StationStateViewSet(viewsets.ModelViewSet):
    serializer_class = StationStateSerializer

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        return StationState.objects.filter(station_id=station_id).order_by("-timestamp")

    @csrf_exempt
    def create(self, request, station_id):
        steering_state = request.data.get('steering_state')

        if steering_state not in ("RM", "ID"):
            return HttpResponseBadRequest("You requested wrong state from this endpoint.")

        manual_steering_user = request.user

        if steering_state == "RM":
            try:
                user = SteeringUser.objects.get().user
                if user == manual_steering_user:
                    return HttpResponse(status=304)

                return HttpResponse(f"User {user.username} is currently in control of the station."
                                    f"You can contact him under {user.email}", status=403)
            except SteeringUser.DoesNotExist:
                pass

            station_url = settings.STATIONS_URLS[station_id]
            response = requests.post(f"{station_url}/manual", headers="Content-Type: application/json",
                                     data=json.dumps(request.data))

            if response.status_code == 200:
                SteeringUser(user=manual_steering_user, station_id=station_id).save()
            elif response.status_code == 403:
                return HttpResponse("Station is in Local Manual mode.", status=403)
            elif response.status_code == 412:
                return HttpResponse("Station is OFF", status=412)
            else:
                return HttpResponse("Unexpected response code from station", status=500)

            Order.objects.create(
                station_id=station_id,
                user=manual_steering_user,
                order="Aquire manual steering"
            )

            return HttpResponse("OK")

        elif steering_state == "ID":
            try:
                SteeringUser.objects.get(user=request.user).delete()
                return HttpResponse("OK")
            except SteeringUser.DoesNotExist:
                try:
                    SteeringUser.objects.get()
                    return HttpResponse("User was not in control of the station.", status=403)
                except SteeringUser.DoesNotExist:
                    return HttpResponse("No user has remote control over station", status=304)


class ValveViewSet(viewsets.ModelViewSet):
    serializer_class = ValveSerializer

    def get_queryset(self):
        return Valve.objects.filter(**self.kwargs).all()


class ValveStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ValveStateSerializer
    filter_backends = [DatetimeRangeFilterBackend]

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        valve_id = self.kwargs['valve_id']
        return ValveState.objects.filter(station_state__station_id=station_id, valve__valve_id=valve_id).order_by(
            "-station_state__timestamp", "-id")

    @csrf_exempt
    def create(self, request, station_id, valve_id):
        try:
            SteeringUser.objects.get(user=request.user, station_id=station_id)
            if StationState.objects.filter(station_id=station_id).latest("timestamp").steering_state != "RM":
                return HttpResponse("User is not in control of the station!")
        except (SteeringUser.DoesNotExist, StationState.DoesNotExist):
            return HttpResponse("User is not in control of the station!")

        station_url = settings.STATIONS_URLS[station_id]
        response = requests.post(f"{station_url}/manual/valve/{valve_id}",
                                 headers="Content-Type: application/json",
                                 data=json.dumps(request.data))

        return HttpResponse(status=response.status_code, content=response.content)


class ContainerViewSet(viewsets.ModelViewSet):
    serializer_class = ContainerSerializer

    def get_queryset(self):
        return Container.objects.filter(**self.kwargs).all()


class ContainerStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContainerStateSerializer
    filter_backends = [DatetimeRangeFilterBackend]

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        container_id = self.kwargs['container_id']
        return ContainerState.objects.filter(station_state__station_id=station_id,
                                             container__container_id=container_id).order_by(
            "-station_state__timestamp", "-id")

    @csrf_exempt
    def create(self, request, station_id, container_id):
        try:
            SteeringUser.objects.get(user=request.user, station_id=station_id)
            if StationState.objects.filter(station_id=station_id).latest("timestamp").steering_state != "RM":
                return HttpResponse("User is not in control of the station!")
        except (SteeringUser.DoesNotExist, StationState.DoesNotExist):
            return HttpResponse("User is not in control of the station!")

        station_url = settings.STATIONS_URLS[station_id]
        response = requests.post(f"{station_url}/manual/container/{container_id}",
                                 headers="Content-Type: application/json",
                                 data=json.dumps(request.data))

        return HttpResponse(status=response.status_code, content=response.content)


class PumpViewSet(viewsets.ModelViewSet):
    serializer_class = PumpSerializer

    def get_queryset(self):
        return Pump.objects.filter(**self.kwargs).all()


class PumpStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PumpStateSerializer
    filter_backends = [DatetimeRangeFilterBackend]

    def get_queryset(self):
        station_id = self.kwargs['station_id']
        pump_id = self.kwargs['pump_id']
        return PumpState.objects.filter(station_state__station_id=station_id, pump__pump_id=pump_id).order_by(
            "-station_state__timestamp", "-id")

    @csrf_exempt
    def create(self, request, station_id, pump_id):
        try:
            SteeringUser.objects.get(user=request.user, station_id=station_id)
            if StationState.objects.filter(station_id=station_id).latest("timestamp").steering_state != "RM":
                return HttpResponse("User is not in control of the station!")
        except (SteeringUser.DoesNotExist, StationState.DoesNotExist):
            return HttpResponse("User is not in control of the station!")

        station_url = settings.STATIONS_URLS[station_id]
        response = requests.post(f"{station_url}/manual/pump/{pump_id}",
                                 headers="Content-Type: application/json",
                                 data=json.dumps(request.data))

        return HttpResponse(status=response.status_code, content=response.content)


@csrf_exempt
def receive_water_data(request, station_id):
    if request.method == 'POST':
        try:
            request_data = json.loads(request.body)
        except JSONDecodeError:
            return HttpResponseBadRequest("Improperly formatted json")

        steering_state = request_data.get("steering_state", None)
        timestamp = request_data["timestamp"]

        manual_steering_user = None
        if steering_state is None:
            last_state = StationState.objects.filter(station_id=station_id).latest("timestamp")
            steering_state = last_state.steering_state
            manual_steering_user = last_state.manual_steering_user
        elif steering_state != "RM":
            try:
                SteeringUser.objects.get(station_id=station_id).delete()
            except SteeringUser.DoesNotExist:
                pass
        elif steering_state == "RM":
            try:
                manual_steering_user = SteeringUser.objects.get(station_id=station_id).user
            except SteeringUser.DoesNotExist:
                steering_state = "ID"

        station_state = StationState.objects.create(
            station_id=station_id,
            timestamp=timestamp,
            steering_state=steering_state,
            manual_steering_user=manual_steering_user
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

    return HttpResponseBadRequest()


@csrf_exempt
def get_steering_states(request):
    if request.method == 'GET':
        return JsonResponse(dict(settings.steering_states))

    return HttpResponseBadRequest()


@csrf_exempt
def automatic(request, station_id):
    if request.method == "POST":
        station_url = settings.STATIONS_URLS[station_id]
        response = requests.post(f"{station_url}/automatic/", data=request.body)
        return HttpResponse(response.text, status=response.status_code)

    return HttpResponseBadRequest()


@csrf_exempt
def config(request, station_id):
    station_url = settings.STATIONS_URLS[station_id]

    if request.method == "GET":
        response = requests.get(f"{station_url}/config/")
        return JsonResponse(response.json, status=response.status_code)

    elif request.method == "PUT":
        response = requests.put(f"{station_url}/config/", data=request.body)
        return JsonResponse(response.json, status=response.status_code)
