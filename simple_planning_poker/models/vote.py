from django.db import models
from django.contrib.auth.models import User

from simple_planning_poker.models.story import Story

class Vote(models.Model):
    story_id = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='votes')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    value = models.CharField(max_length=10) 
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story_id', 'user_id')

    def __str__(self):
        return f"{self.user_id.username} voted {self.value} on {self.story_id.title}"