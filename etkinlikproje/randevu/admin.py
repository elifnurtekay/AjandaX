from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('category', 'attendee', 'start_time', 'notes', 'created_at')
    list_filter = ('category', 'attendee', 'start_time')
    search_fields = ('attendee__username', 'notes')

admin.site.register(Appointment, AppointmentAdmin)
