from django.db import models
from djgeojson.fields import PointField

from core.mixins import AbstractTrack


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
