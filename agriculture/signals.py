from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone

from .models import LoginHistory


@receiver(user_logged_in)
def record_user_login(sender, request, user, **kwargs):
    if user is None or not user.is_authenticated:
        return

    # Create a login record
    history = LoginHistory.objects.create(
        user=user,
        login_time=timezone.now()
    )

    # Remember this login record for logout tracking
    if request is not None:
        request.session["login_history_id"] = history.id


@receiver(user_logged_out)
def record_user_logout(sender, request, user, **kwargs):
    if request is None:
        return

    history_id = request.session.get("login_history_id")

    if history_id:
        LoginHistory.objects.filter(
            id=history_id,
            logout_time__isnull=True
        ).update(
            logout_time=timezone.now()
        )