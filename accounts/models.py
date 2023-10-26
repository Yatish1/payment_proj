from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class user_profile(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.BigIntegerField()

