from .models import TrackEvent, Track, TrackableEvent
from django.http import JsonResponse
import json
from user_agents import parse as user_agent_parser
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

# Create your views here.


@csrf_exempt
def track(request):
    event_data = json.loads(request.body)
    event_type = event_data.get("eventType", None)
    track_id = event_data.get("trackId", None)
    track = Track.objects.filter(track_id=track_id)
    if track.exists():
        track = track[0]
        if not track.active:
            return JsonResponse({"error": "Track is not active"}, status=400)
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid track id"}, status=400
        )

    event_name = event_data.get("eventName", None)
    user_agent = request.META.get("HTTP_USER_AGENT", None)
    user_agent_data = user_agent_parser(user_agent)
    origin = request.META.get("HTTP_ORIGIN", None)
    trackable_event = TrackableEvent.objects.filter(
        name=event_name, type=event_type, track_id=track
    )
    if trackable_event.exists():
        trackable_event = trackable_event[0]
    else:
        trackable_event = TrackableEvent.objects.filter(type=event_type, track_id=track)
        if trackable_event.exists():
            trackable_event = trackable_event[0]
        else:
            return JsonResponse({"success": False, "error": "Invalid event type"})

    TrackEvent.objects.create(
        track_id=track,
        event=trackable_event,
        ip_address=request.META.get("REMOTE_ADDR"),
        user_agent=user_agent,
        device_type=user_agent_data.device.family,
        browser=user_agent_data.browser.family,
        domain=origin,
        os=user_agent_data.os.family,
    )
    return JsonResponse({"status": "ok"})


def get_track_events(request, trackId):
    track = Track.objects.filter(track_id=trackId)
    if not track.exists():
        return JsonResponse(
            {"status": "error", "message": "Invalid track id"}, status=400
        )

    trackable_events = TrackableEvent.objects.filter(track_id=track[0])

    return JsonResponse(
        {
            "status": "ok",
            "data": [
                {
                    "name": event.name,
                    "type": event.type,
                    "html_id": event.html_id,
                    "html_class": event.html_class,
                    "html_tag": event.html_tag,
                    "html_selector": event.html_selector,
                }
                for event in trackable_events
            ],
        }
    )


def get_track_data(request, trackId):
    track = Track.objects.filter(track_id=trackId)
    if track.exists() and track[0].user == request.user:
        track = track[0]

        # Get the events group by timestamp with only date and count
        events = (
            TrackEvent.objects.filter(track_id=track)
            .extra(select={"date": "date(timestamp)"})
            .values("date")
            .annotate(count=Count("id"))
        )

        trackable_events = TrackableEvent.objects.filter(track_id=track)
        data = []
        # For every event create a list of total number of events vs timestamp
        for trackable_event in trackable_events:
            event_data = []
            for event in events.filter(event=trackable_event):
                event_data.append(
                    {
                        "x": event["date"],
                        "y": event["count"],
                    }
                )
            data.append(
                {
                    "name": trackable_event.name,
                    "type": trackable_event.type,
                    "data": event_data,
                }
            )

        return JsonResponse({"status": "ok", "data": data})
    return JsonResponse({"status": "error", "message": "Invalid track id"}, status=400)
