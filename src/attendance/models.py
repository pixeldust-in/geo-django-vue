from typing import List

from django.db import models
from djgeojson.fields import PointField

from core.mixins import AbstractTrack
from services.location import get_location_from_coords


# Create your models here.
class Attendance(AbstractTrack):
    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="attendance"
    )
    date = models.DateField()
    check_in = models.TimeField()
    check_out = models.TimeField(null=True, blank=True)
    location = PointField()
    location_meta = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        unique_together = ("user", "date")

    def __str__(self) -> str:
        return f"{self.user.full_name} - {self.date}"

    def save(self, *args, **kwargs):
        if not self.pk:
            lat, lng = self.location["coordinates"]
            self.location_meta = get_location_from_coords(lat, lng)
        super().save(*args, **kwargs)

    def formatted_address(self) -> str:
        return self.location_meta.get("formatted_address", "")
