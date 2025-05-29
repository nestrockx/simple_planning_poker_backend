import random
import string
from django.db import models
from django.contrib.auth.models import User

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class Room(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True, default=generate_code)
    type = models.CharField(max_length=20, choices=[('default', 'Default'), ('fibonacci', 'Fibonacci'), ('tshirts', 'Tshirts'), ('powers', 'Powers')], default='default')
    participants = models.ManyToManyField(User, related_name='joined_rooms', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

# moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderated_rooms', blank=True)