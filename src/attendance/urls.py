from django.urls import path
from rest_framework import routers

from . import api

app_name = "attendance"

router = routers.DefaultRouter()

router.register("user-attedance", api.UserAttendanceViewSet, basename="user-attedance")
# urlpatterns = [
#     path("user-attedance", api.user-attedance.as_view({'get': 'list'}), name="user-attedance"),
# ]
urlpatterns = []
