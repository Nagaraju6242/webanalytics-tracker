from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from track.views import track, get_track_events, get_track_data
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/track/", track),
    path("api/track/<str:trackId>/data/", get_track_data),
    path("api/trackable_events/<str:trackId>/", get_track_events),
    path("", home, name="home"),
    path("accounts/login/", login, name="login"),
    path("accounts/register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/track/<str:trackId>/", track_dashboard, name="track_dashboard"),
    path("api/tracker/create/", create_tracker),
    path("api/logs/import/", import_logs, name="import_logs"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
