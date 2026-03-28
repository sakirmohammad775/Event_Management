from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=225)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="events"
    )
    asset = CloudinaryField('image', default='default_img')
    # asset = models.ImageField(
    #     upload_to="events_asset/",
    #     blank=True,
    #     default="defaults/default_img.png"   # ← relative to MEDIA_ROOT
    # )
    participants = models.ManyToManyField(
        User,
        related_name="rsvp_events",
        blank=True
    )

    def __str__(self):
        return self.name