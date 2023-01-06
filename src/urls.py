from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework import routers

from attendance.urls import router as attendance_router

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.registry.extend(attendance_router.registry)

urlpatterns = [
    path("super-manager/", admin.site.urls),
    # apps
    path("api/", include(router.urls)),
    path("api/attendance/", include("attendance.urls")),
    re_path(r"app.*", TemplateView.as_view(template_name="app.html"), name="home"),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
