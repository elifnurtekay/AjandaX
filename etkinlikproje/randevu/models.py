from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    CATEGORY_CHOICES = [
        ('danismanlik', 'Danışmanlık'),
        ('saglik', 'Sağlık'),
        ('gorusme', 'Görüşme'),
        ('mulakat', 'Mülakat'),
        ('diger', 'Diğer'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    attendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # user alanına gerek yok, attendee zaten kullanıcıyı temsil ediyor. İstersen kaldırabilirsin.
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # GEREK YOK

    def __str__(self):
        return f"{self.attendee.username} ({self.get_category_display()})"
