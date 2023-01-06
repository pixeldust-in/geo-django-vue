from django.utils.timezone import datetime
from drf_extra_fields.geo_fields import PointField
from rest_framework import serializers

from . import models


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        for field in fields:
            fields[field].read_only = True
        return fields


class UserAttendanceListSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = models.Attendance
        exclude = (
            "id",
            "created",
            "modified",
            "user",
            "location_meta",
        )


class UserAttendanceCheckinSerializer(serializers.ModelSerializer):
    def validate(self, data):
        date = data.get("date")
        if date != datetime.today():
            raise serializers.ValidationError(
                {"message": "You can only check in today!"}
            )
        return data

    class Meta:
        model = models.Attendance
        exclude = (
            "id",
            "created",
            "modified",
            "user",
            "location_meta",
            "check_out",
        )


class UserAttendanceCheckoutSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if self.instance.check_out:
            raise serializers.ValidationError(
                {"message": "You have already checked out!"}
            )
        return data

    class Meta:
        model = models.Attendance
        fields = ("check_out",)
