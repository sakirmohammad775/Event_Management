from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from events.models import Event
from django.contrib.auth import get_user_model


@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        User = get_user_model()
        for user_pk in pk_set:
            try:
                user = User.objects.get(pk=user_pk)
                send_mail(
                    subject=f"RSVP Confirmed: {instance.name}",
                    message=(
                        f"Hi {user.username},\n\n"
                        f"Your RSVP for '{instance.name}' on {instance.date} "
                        f"at {instance.location} is confirmed!\n\nSee you there!"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except User.DoesNotExist:
                pass