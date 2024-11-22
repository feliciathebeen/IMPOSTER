from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=20) 
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20, unique=True)
    birth = models.DateField(null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, default="default_profile.png")

    def __str__(self):
        return self.username
