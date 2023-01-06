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
    formatted_address = serializers.CharField()

    class Meta:
        model = models.Attendance
        exclude = ("id", "created", "modified", "user", "location", "location_meta")


def today_date():
    return datetime.today().date()


def current_time():
    return datetime.now().strftime("%H:%M:%S")


class UserAttendanceCheckinSerializer(serializers.ModelSerializer):
    date = serializers.DateField(default=today_date)
    check_in = serializers.DateTimeField(default=current_time)

    def validate(self, data):
        date = data.get("date")
        if date != datetime.today().date():
            raise serializers.ValidationError(
                {"message": "You can check in for today only!"}
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
    check_out = serializers.DateTimeField(default=current_time)

    def validate(self, data):
        if self.instance.check_out:
            raise serializers.ValidationError(
                {"message": "You have already checked out!"}
            )
        if self.instance.date != datetime.today().date():
            raise serializers.ValidationError(
                {"message": "You can check out for today only!"}
            )
        return data

    class Meta:
        model = models.Attendance
        fields = ("check_out",)
