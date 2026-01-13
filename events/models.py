from django.db import models


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


class Participant(models.Model):
    # Participate details
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    # A participant can join many events
    # An event can hav Many participants
    events = models.ManyToManyField(Event, related_name="participants", blank=True)

    def __str__(self):
        return self.name
