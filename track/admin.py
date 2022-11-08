from django.contrib import admin
from .models import Track, TrackEvent, TrackableEvent

# Register your models here.
class TrackAdmin(admin.ModelAdmin):
    list_display = ["track_id", "user", "track_name", "active"]


class TrackClickAdmin(admin.ModelAdmin):
    list_display = ["track_id", "get_name", "get_type", "timestamp"]

    def get_name(self, obj):
        return obj.event.name

    get_name.admin_order_field = "Name"  # Allows column order sorting
    get_name.short_description = "Name"  # Renames column head

    def get_type(self, obj):
        return obj.event.type

    get_type.admin_order_field = "Type"  # Allows column order sorting
    get_type.short_description = "Type"  # Renames column head


class TrackableEventAdmin(admin.ModelAdmin):
    list_display = ["track_id", "name", "type", "html_id", "html_class"]


admin.site.register(Track, TrackAdmin)
admin.site.register(TrackEvent, TrackClickAdmin)
admin.site.register(TrackableEvent, TrackableEventAdmin)
