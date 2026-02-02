from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    # Event basic information
    name = models.CharField(max_length=200)
    description = models.TextField()

    # Event schedule
    date = models.DateField()
    time = models.TimeField()

    # Event location
    location = models.CharField(max_length=225)

    # Each event belongs to one category
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="events"
    )

    def __str__(self):
        return self.name

    asset = models.ImageField(
        upload_to="events_asset", 
        blank=True, null=True
    )
    participants =models.ManyToManyField(
        User, 
        related_name="rsvp_events",
        blank = True
    )

    def __str__(self):
        return self.name
