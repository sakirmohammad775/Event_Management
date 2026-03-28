from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()


# ─────────────────────────────────────────────
#  PROBLEM 1 FIX: token generated BEFORE save
#  → token is now generated AFTER user.save()
#  using post_save with created=True
#
#  PROBLEM 2 FIX: removed assign_role signal
#  → role is assigned in SignUpView directly
#  → signal was causing double-save which
#    invalidates the token immediately
# ─────────────────────────────────────────────

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if not created:
        return  # only on new user creation

    # Skip sending email to superusers (created via createsuperuser)
    if instance.is_superuser:
        return

    # Skip if no email address
    if not instance.email:
        return

    token = default_token_generator.make_token(instance)
    activation_url = (
        f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
    )

    subject = "Activate Your EventHub Account"
    message = (
        f"Hi {instance.username},\n\n"
        f"Welcome to EventHub! Please activate your account by clicking the link below:\n\n"
        f"{activation_url}\n\n"
        f"This link will expire after first use.\n\n"
        f"If you did not create this account, please ignore this email.\n\n"
        f"— The EventHub Team"
    )

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False,   # ← False so errors are visible in logs
        )
        print(f"[Signal] Activation email sent to {instance.email}")
    except Exception as e:
        print(f"[Signal] Failed to send activation email to {instance.email}: {e}")


# ─────────────────────────────────────────────
#  RSVP confirmation email
#  Fires when a user is added to event.participants
# ─────────────────────────────────────────────

def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action != "post_add" or not pk_set:
        return

    for user_pk in pk_set:
        try:
            user = User.objects.get(pk=user_pk)
            subject = f"RSVP Confirmed: {instance.name}"
            message = (
                f"Hi {user.username},\n\n"
                f"Your RSVP for '{instance.name}' is confirmed!\n\n"
                f"📅 Date: {instance.date}\n"
                f"⏰ Time: {instance.time}\n"
                f"📍 Location: {instance.location}\n\n"
                f"See you there!\n\n"
                f"— The EventHub Team"
            )
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=True,
            )
            print(f"[Signal] RSVP email sent to {user.email}")
        except User.DoesNotExist:
            pass
        except Exception as e:
            print(f"[Signal] Failed to send RSVP email: {e}")


# Connect RSVP signal — imported here to avoid circular import
def connect_rsvp_signal():
    try:
        from events.models import Event
        m2m_changed.connect(send_rsvp_email, sender=Event.participants.through)
        print("[Signal] RSVP signal connected")
    except Exception as e:
        print(f"[Signal] Could not connect RSVP signal: {e}")