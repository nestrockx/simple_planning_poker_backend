# Generated by Django 5.1.7 on 2025-04-08 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_planning_poker', '0002_room_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.CharField(choices=[('default', 'Default'), ('fibonacci', 'Fibonacci')], default='default', max_length=20),
        ),
    ]
