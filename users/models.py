from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):

    profile_picture = CloudinaryField('image', default='default')
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )