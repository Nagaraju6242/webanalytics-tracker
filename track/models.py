from django.db import models
from django.contrib.auth.models import User
from tracker.utils import id_generator
from django.utils import timezone

# Create your models here.
EVENT_TYPE = (
    ("click", "Click"),
    ("pageview", "Pageview"),
)


class Track(models.Model):
    track_id = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.track_id

    # Automatically generate a random track_id
    def save(self, *args, **kwargs):
        if not self.track_id:
            self.track_id = id_generator(size=10)
            while Track.objects.filter(track_id=self.track_id).exists():
                self.track_id = self.id_generator(size=10)
        super(Track, self).save(*args, **kwargs)


class TrackableEvent(models.Model):
    track_id = models.ForeignKey(Track, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=EVENT_TYPE)
    html_id = models.CharField(max_length=100, null=True, blank=True)
    html_class = models.CharField(max_length=100, null=True, blank=True)
    html_tag = models.CharField(max_length=100, null=True, blank=True)
    html_selector = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # If selector is not present create selector from tag class and id
        if not self.html_selector:
            self.html_selector = ""
            if self.html_tag:
                self.html_selector += self.html_tag
            if self.html_class:
                self.html_selector += "." + self.html_class
            if self.html_id:
                self.html_selector += "#" + self.html_id
        super(TrackableEvent, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class TrackEvent(models.Model):
    track_id = models.ForeignKey(Track, on_delete=models.CASCADE)
    event = models.ForeignKey(TrackableEvent, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=40)

    user_agent = models.CharField(max_length=200, null=True)
    device_type = models.CharField(max_length=100, null=True)
    browser = models.CharField(max_length=100, null=True)
    os = models.CharField(max_length=100, null=True)
    domain = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)

    def get_name(self):
        return self.event.name + "  --  " + str(self.event.type)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self) -> str:
        return self.event.name + "  --  " + str(self.event.type)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        super(TrackEvent, self).save(*args, **kwargs)
