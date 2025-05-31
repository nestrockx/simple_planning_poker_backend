from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = "Deletes guest users older than 2 days"

    def handle(self, *args, **kwargs):
        threshold = timezone.now() - timedelta(days=2)
        guests = User.objects.filter(username__startswith='guest_', date_joined__lt=threshold)
        count = guests.count()
        guests.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} old guest user(s)."))
