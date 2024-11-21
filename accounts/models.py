from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=20) 
    last_name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    birth = models.DateField(null=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True)

    def __str__(self):
        return self.username
