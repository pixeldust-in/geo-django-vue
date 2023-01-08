from typing import List

from django.contrib.gis.db.models import PointField
from django.db import models
from geopy.distance import lonlat

from core.mixins import AbstractTrack
from services.geo import get_location_from_coords


# Create your models here.
class Attendance(AbstractTrack):
    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="attendance"
    )
    date = models.DateField()
    check_in = models.TimeField()
    check_out = models.TimeField(null=True, blank=True)
    location = PointField(srid=4326, null=True, blank=True)
    location_meta = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        unique_together = ("user", "date")

    def __str__(self) -> str:
        return f"{self.user.full_name} - {self.date}"

    def save(self, *args, **kwargs):
        if not self.pk and self.location and self.location.coords:
            lng, lat = list(self.location.coords)
            self.location_meta = get_location_from_coords(lat, lng)
        super().save(*args, **kwargs)

    def formatted_address(self) -> str:
        return self.location_meta.get("formatted_address", "")

    @property
    def lat_lng(self) -> List[float]:
        if self.location and self.location.coords:
            lng, lat = list(self.location.coords)
            return [lat, lng]
        return None
