from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models


def validate_file_size(file):
    max_size = 2 * 1024 * 1024  # 2MB
    if file.size > max_size:
        raise ValidationError("Image must be smaller than 2MB.")


class CustomUser(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    streak = models.IntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True,
        validators=[validate_file_size],
    )
    birthdate = models.DateField(blank=True, null=True, verbose_name="Date of Birth")

    class Meta:
        ordering = ["user__username"]
        indexes = [models.Index(fields=["user"])]

    def __str__(self):
        return f"{self.user.username}'s profile"
