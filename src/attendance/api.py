from django.db import IntegrityError
from django.utils.timezone import datetime
from rest_framework import permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from attendance.serializers import (
    UserAttendanceCheckinSerializer,
    UserAttendanceCheckoutSerializer,
    UserAttendanceListSerializer,
)

from .models import Attendance


class UserAttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = UserAttendanceListSerializer
    queryset = Attendance.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "uuid"
    http_method_names = [
        "get",
        "post",
        "put",
    ]
    action_serializers = {
        "list": UserAttendanceListSerializer,
        "create": UserAttendanceCheckinSerializer,
        "retrieve": UserAttendanceListSerializer,
        "update": UserAttendanceCheckoutSerializer,
    }

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=user)

        return qs

    def get_serializer_class(self):
        if self.action in self.action_serializers:
            return self.action_serializers[self.action]
        return UserAttendanceListSerializer

    def perform_create(self, serializer, *args, **kwargs):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"message": "You have already checked in today!"}
            )

    @action(methods=["GET"], detail=False, url_path="today")
    def today_status(self, requst, *args, **kwargs):
        try:
            today = super().get_queryset(*args, **kwargs).get(date=datetime.today())
            data = UserAttendanceListSerializer(today).data
        except Attendance.DoesNotExist:
            data = None
        return Response({"data": data})
