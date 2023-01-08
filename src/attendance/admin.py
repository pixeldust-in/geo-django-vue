from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Attendance


# Register your models here.
@admin.register(Attendance)
class UserAdmin(LeafletGeoAdmin):
    list_display = ("user", "date", "check_in", "check_out")
    search_fields = ("user__full_name",)
    list_filter = ("date",)
    fields = ("date", "user", "check_in", "check_out", "location", "location_meta")
