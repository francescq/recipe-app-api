from django.test import TestCase
from django.contrib.auth import get_user_model

from unittest.mock import patch

from core import models


def sample_user(email='an@email.com', password='password'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), 'Vegan')

    def test_ingredient_str(self):
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), 'Cucumber')

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Bravas',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), 'Bravas')

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        mock_uuid.return_value = 'test-uuid'
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        self.assertEqual(file_path, 'uploads/recipe/{}.jpg'.format(mock_uuid))
