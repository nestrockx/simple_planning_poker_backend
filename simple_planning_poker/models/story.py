from django.db import models

from simple_planning_poker.models.room import Room

class Story(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=255, default='Story')
    is_active = models.BooleanField(default=False)
    is_revealed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title