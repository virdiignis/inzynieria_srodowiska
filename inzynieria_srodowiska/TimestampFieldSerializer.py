import datetime
import time

from rest_framework import serializers


class TimestampField(serializers.DateTimeField):
    @staticmethod
    def to_native(value):
        """ Return epoch time for a datetime object or ``None``"""
        try:
            return time.mktime(value.timetuple())
        except (AttributeError, TypeError):
            return None

    @staticmethod
    def from_native(value):
        return datetime.datetime.fromtimestamp(value)


class RelatedTimestampField(serializers.SlugRelatedField, TimestampField):
    def to_representation(self, obj):
        return self.to_native(obj.timestamp)
