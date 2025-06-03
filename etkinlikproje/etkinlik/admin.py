from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_time', 'end_time', 'location', 'created_at')
    list_filter = ('category', 'start_time')
    search_fields = ('title', 'description', 'location')

admin.site.register(Event, EventAdmin)

