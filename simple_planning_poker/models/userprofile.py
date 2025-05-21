from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    moderator = models.BooleanField(default=False)
    nickname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nickname or self.user.username