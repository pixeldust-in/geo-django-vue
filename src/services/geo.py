from django.conf import settings
from geopy.geocoders import GoogleV3


def get_location_from_coords(lat, lng):
    if not settings.GOOGLE_MAPS_API_KEY:
        return {}
    geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
    location = geolocator.reverse(f"{lat}, {lng}")
    return location.raw
