from django.db import models
from django.conf import settings
from django.contrib.auth.models import User




class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, through='EventRegistration',
                                       related_name='attending_events')

    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
