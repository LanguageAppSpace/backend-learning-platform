from datetime import date
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image
from rest_framework.test import APIRequestFactory

from user.models import Profile
from user.serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    CustomUserSerializer,
    PasswordResetConfirmSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    UserStreakSerializer,
)

User = get_user_model()


class RegisterSerializerTests(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!",
        }

    def test_valid_registration(self):
        serializer = RegisterSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_duplicate_email_returns_custom_error_message(self):
        User.objects.create_user(
            username="existinguser",
            email="test@example.com",
            password="StrongPassword123!",
        )

        serializer = RegisterSerializer(data=self.valid_data)

        self.assertFalse(serializer.is_valid())

        self.assertEqual(
            serializer.errors["email"][0],
            "An account with this email address already exists.",
        )

    def test_password_confirmation_must_match(self):
        data = self.valid_data.copy()
        data["password_confirm"] = "DifferentPassword123!"

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertEqual(
            serializer.errors["password"][0],
            "Passwords don't match.",
        )

    def test_invalid_password_is_rejected(self):
        data = self.valid_data.copy()
        data["password"] = "123"
        data["password_confirm"] = "123"

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_password_is_not_returned(self):
        serializer = RegisterSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertNotIn("password", serializer.data)
        self.assertNotIn("password_confirm", serializer.data)
        self.assertTrue(user.check_password("StrongPassword123!"))


class CustomTokenObtainPairSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPassword123!",
        )

    def test_token_contains_username_and_email(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)

        self.assertEqual(token["username"], self.user.username)
        self.assertEqual(token["email"], self.user.email)


class ChangePasswordSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="OldPassword123!",
        )

        factory = APIRequestFactory()
        request = factory.patch("/user/change-password/")
        request.user = self.user

        self.context = {"request": request}

    def test_valid_password_change(self):
        data = {
            "old_password": "OldPassword123!",
            "new_password": "NewPassword123!",
            "new_password_confirm": "NewPassword123!",
        }

        serializer = ChangePasswordSerializer(
            instance=self.user,
            data=data,
            context=self.context,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        serializer.save()

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password("NewPassword123!"))
        self.assertFalse(self.user.check_password("OldPassword123!"))

    def test_wrong_old_password(self):
        data = {
            "old_password": "WrongPassword123!",
            "new_password": "NewPassword123!",
            "new_password_confirm": "NewPassword123!",
        }

        serializer = ChangePasswordSerializer(
            instance=self.user,
            data=data,
            context=self.context,
        )

        self.assertFalse(serializer.is_valid())

        self.assertIn("old_password", serializer.errors)

    def test_new_passwords_must_match(self):
        data = {
            "old_password": "OldPassword123!",
            "new_password": "NewPassword123!",
            "new_password_confirm": "DifferentPassword123!",
        }

        serializer = ChangePasswordSerializer(
            instance=self.user,
            data=data,
            context=self.context,
        )

        self.assertFalse(serializer.is_valid())

        self.assertEqual(
            serializer.errors["new_password"][0],
            "Passwords do not match.",
        )


class PasswordResetConfirmSerializerTests(TestCase):
    def test_matching_passwords_are_valid(self):
        data = {
            "new_password": "NewStrongPassword123!",
            "confirm_new_password": "NewStrongPassword123!",
            "token": "some-reset-token",
        }

        serializer = PasswordResetConfirmSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_passwords_must_match(self):
        data = {
            "new_password": "NewStrongPassword123!",
            "confirm_new_password": "DifferentPassword123!",
            "token": "some-reset-token",
        }

        serializer = PasswordResetConfirmSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn(
            "The new password and the confirmed password do not match.",
            str(serializer.errors),
        )

    def test_weak_password_is_rejected(self):
        data = {
            "new_password": "123",
            "confirm_new_password": "123",
            "token": "some-reset-token",
        }

        serializer = PasswordResetConfirmSerializer(data=data)

        self.assertFalse(serializer.is_valid())


class CustomUserSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPassword123!",
        )

    def test_serializes_expected_fields(self):
        serializer = CustomUserSerializer(self.user)

        self.assertEqual(
            set(serializer.data.keys()),
            {
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "streak",
                "last_active",
            },
        )


class ProfileSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPassword123!",
        )
        self.profile = Profile.objects.create(
            user=self.user,
            birthdate=date(1990, 1, 1),
        )

    def test_profile_contains_user_data(self):
        serializer = ProfileSerializer(self.profile)

        self.assertEqual(serializer.data["user"]["username"], "testuser")
        self.assertEqual(serializer.data["user"]["email"], "test@example.com")

    def test_profile_user_is_read_only(self):
        serializer = ProfileSerializer(self.profile)

        self.assertTrue(serializer.fields["user"].read_only)


class ProfileUpdateSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPassword123!",
        )
        self.profile = Profile.objects.create(user=self.user)

    def create_image(self, image_format="JPEG"):
        image = Image.new("RGB", (100, 100))

        image_file = BytesIO()
        image.save(image_file, format=image_format)
        image_file.seek(0)

        extension = "jpg" if image_format == "JPEG" else "png"
        content_type = "image/jpeg" if image_format == "JPEG" else "image/png"

        return SimpleUploadedFile(
            f"test.{extension}",
            image_file.read(),
            content_type=content_type,
        )

    def test_valid_jpeg_is_accepted(self):
        image = self.create_image("JPEG")

        serializer = ProfileUpdateSerializer(
            instance=self.profile,
            data={"photo": image},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_valid_png_is_accepted(self):
        image = self.create_image("PNG")

        serializer = ProfileUpdateSerializer(
            instance=self.profile,
            data={"photo": image},
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_non_image_content_type_is_rejected(self):
        file = SimpleUploadedFile(
            "test.txt",
            b"not an image",
            content_type="text/plain",
        )

        serializer = ProfileUpdateSerializer(
            instance=self.profile,
            data={"photo": file},
        )

        self.assertFalse(serializer.is_valid())

    def test_invalid_image_file_is_rejected(self):
        file = SimpleUploadedFile(
            "test.jpg",
            b"this is not actually an image",
            content_type="image/jpeg",
        )

        serializer = ProfileUpdateSerializer(
            instance=self.profile,
            data={"photo": file},
        )

        self.assertFalse(serializer.is_valid())


class UserStreakSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPassword123!",
        )

    def test_serializes_streak_data(self):
        self.user.streak = 5
        self.user.last_active = date(2026, 6, 10)
        self.user.save()

        serializer = UserStreakSerializer(self.user)

        self.assertEqual(serializer.data["streak"], 5)
        self.assertEqual(serializer.data["last_active"], "2026-06-10")
