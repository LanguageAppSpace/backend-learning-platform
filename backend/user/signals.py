import os

from django.dispatch import receiver
from django.core.mail import EmailMessage
from django_rest_passwordreset.signals import reset_password_token_created

from .utils import CustomTokenGenerator

custom_token_generator = CustomTokenGenerator()


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    custom_token = custom_token_generator.generate_token()
    reset_password_token.key = custom_token
    reset_password_token.save()

    context = {
        "current_user": reset_password_token.user,
        "username": reset_password_token.user.username,
        "email": reset_password_token.user.email,
        # pylint: disable=consider-using-f-string
        "reset_password_url": "{}?token={}".format(
            "https://project-language-app.netlify.app/reset-password",
            reset_password_token.key,
        ),
    }

    email_msg = (
        f"Hello {context['username']}, "
        f"We've received a request to reset your password. "
        f"Please click on the link below to reset your password: "
        f"{context['reset_password_url']}"
    )

    msg = EmailMessage(
        f"Password reset for {context['email']}",
        email_msg,
        os.getenv("DEFAULT_FROM_EMAIL"),
        [reset_password_token.user.email],
    )
    msg.send()
