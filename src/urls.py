from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import include, path, re_path
from rest_framework import routers

from attendance.urls import router as attendance_router
from core import views as core_views

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.registry.extend(attendance_router.registry)

urlpatterns = [
    path("super-manager/", admin.site.urls),
    # Thirdparty
    path("auth/signup/", core_views.notfoundview),
    path("auth/", include("allauth.urls")),
    # apps
    path("api/", include(router.urls)),
    path("api/attendance/", include("attendance.urls")),
    path("", core_views.root, name="home_redirect"),
    re_path(r"^app.*", core_views.home, name="home"),
    path(
        "accounts/login/",
        LoginView.as_view(
            template_name="admin/login.html",
            extra_context={
                "site_header": "Geo Attendance App",
            },
        ),
    ),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
