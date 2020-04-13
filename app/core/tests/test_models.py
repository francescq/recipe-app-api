from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """should create a new user with an email"""
        email = 'an@email.com'
        password = 'pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """email text is normalized"""
        email = "an@EMAIL.COM"
        user = get_user_model().objects.create_user(email, 'fooPassword')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """should fail when no emal"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'foopass')

    def test_create_superuser(self):
        """should create a super user"""
        user = get_user_model().objects.create_superuser(
            'an@email.com',
            'foopassed'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)