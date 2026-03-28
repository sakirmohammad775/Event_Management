from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        import users.signals                 # registers activation email signal
        users.signals.connect_rsvp_signal()  # registers RSVP email signal