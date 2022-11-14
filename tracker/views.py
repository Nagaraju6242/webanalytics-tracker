from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from track.models import Track, TrackableEvent, TrackEvent
from track.forms import TrackableEventForm
import apache_log_parser
from user_agents import parse as user_agent_parser
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login, authenticate
from tracker.utils import get_frontend_snippet


def home(request):
    return render(request, "tracker/home.html")


@login_required
def dashboard(request):
    tracks = Track.objects.filter(user=request.user)
    print(tracks)
    return render(request, "tracker/dashboard.html", {"tracks": tracks})


def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
    return render(request, "tracker/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password)
        user.save()
        auth_login(request, user)
        return redirect("dashboard")
    return render(request, "tracker/login.html")


@login_required
def logout(request):
    auth_logout(request)
    return redirect("home")


@login_required
def create_tracker(request):
    if request.method == "POST" and request.POST.get("track_name"):
        track = Track(track_name=request.POST.get("track_name"), user=request.user)
        track.save()
    return redirect("dashboard")


@login_required
def track_dashboard(request, trackId):
    track = Track.objects.get(track_id=trackId)
    if track.user != request.user:
        return redirect("dashboard")

    trackable_events = TrackableEvent.objects.filter(track_id=track)
    track_events = TrackEvent.objects.filter(track_id=track)

    trackable_events_form = TrackableEventForm(request.POST or None)
    if request.method == "POST" and trackable_events_form.is_valid():
        if trackable_events_form.cleaned_data["track_id"] == track:
            trackable_events_form.save()
        return redirect("track_dashboard", trackId=trackId)

    trackable_events_form.fields["track_id"].initial = track
    frontend_snippet_code = get_frontend_snippet(trackId)

    return render(
        request,
        "tracker/track_dashboard.html",
        {
            "track": track,
            "trackable_events": trackable_events,
            "track_events": track_events,
            "trackable_events_form": trackable_events_form,
            "frontend_snippet_code": frontend_snippet_code,
        },
    )


def import_logs(request):
    if request.method == "POST":
        track_id = request.POST.get("track_id")
        track = Track.objects.get(track_id=track_id)
        if track.user != request.user:
            return redirect("dashboard")
        # get the uploaded file
        print(request.FILES)
        # return JsonResponse({"success": True})
        log_file = request.FILES["log_file"]
        # read the file
        logs = log_file.read().decode("utf-8").split("\n")

        # 209.126.136.4 - - [27/Dec/2017:12:00:00 +0000] "GET /cart/checkout HTTP/1.1" 303 5005 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        log_parser = apache_log_parser.make_parser(
            '%h - - %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i"'
        )

        for log in logs:
            if log.strip().replace("\n", "") == "":
                continue
            parsed_log = log_parser(log)
            user_agent = user_agent_parser(parsed_log["request_header_user_agent"])
            track_event = TrackEvent(
                track_id=track,
                event=get_or_create_pageviewEvent(track),
                ip_address=parsed_log["remote_host"],
                user_agent=parsed_log["request_header_user_agent"],
                domain="",
                device_type=user_agent.device.family,
                browser=user_agent.browser.family,
                os=user_agent.os.family,
                timestamp=parsed_log["time_received_datetimeobj"],
            )
            track_event.save()
    return JsonResponse({"success": True})


def get_or_create_pageviewEvent(track):
    pageview_event = TrackableEvent.objects.filter(
        track_id=track, name="Pageview"
    ).first()
    if not pageview_event:
        pageview_event = TrackableEvent(
            track_id=track, name="Pageview", type="pageview"
        )
        pageview_event.save()
    return pageview_event
