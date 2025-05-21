from django.apps import AppConfig

class SimplePlanningPokerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simple_planning_poker'

    def ready(self):
        import simple_planning_poker.signals