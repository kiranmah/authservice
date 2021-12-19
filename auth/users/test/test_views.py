import factory
import json
from faker import Faker
import unittest
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from ..models import User
from .factories import UserFactory

fake = Faker()


class TestUserCreate(APITestCase):
    """
    Tests POST /users/
    """

    def setUp(self):
        self.url = reverse("user-list")
        self.test_data = {
            "username": "test-user-1",
            "password": "test-password",
            "first_name": "test-fname",
            "last_name": "test-lname",
        }

    def test_valid_post_request_creates_user(self):
        response = self.client.post(self.url, self.test_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get()
        self.assertEquals(user.username, self.test_data["username"])
        self.assertEquals(user.first_name, self.test_data["first_name"])
        self.assertEquals(user.last_name, self.test_data["last_name"])

    def test_valid_post_request_does_not_create_duplicate_user(self):
        response = self.client.post(self.url, self.test_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(User.objects.count(), 1)
        response = self.client.post(self.url, self.test_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(User.objects.count(), 1)

    def test_post_request_with_incomplete_data_does_not_create_user(self):
        self.test_data["password"] = ""
        response = self.client.post(self.url, self.test_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(
            json.loads(response.content),
            {"password": ["This field may not be blank."]},
        )
        self.assertEquals(User.objects.count(), 0)


class TestUserUpdate(APITestCase):
    """
    Tests PUT + PATCH /users/pk:uuid
    """

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse("user-detail", kwargs={"pk": self.user.pk})

    def test_valid_patch_request_updates_user(self):
        data = {"first_name": fake.first_name()}

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer  {refresh.access_token}")
        response = self.client.patch(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        user = User.objects.get()
        self.assertEquals(user.first_name, data["first_name"])
    
    def test_invalid_patch_request_returns_correct_responses(self):
        data = {"first_name": fake.first_name()}
        response = self.client.patch(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer  fake-token")
        response = self.client.patch(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get()
        self.assertNotEquals(user.first_name, data["first_name"])

    def test_valid_put_request_updates_user(self):
        data = {"first_name": fake.first_name()}

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer  {refresh.access_token}")
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        user = User.objects.get()
        self.assertEquals(user.first_name, data["first_name"])
    
    def test_invalid_put_request_returns_correct_responses(self):
        data = {"first_name": fake.first_name()}
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer  fake-token")
        response = self.client.put(self.url, data)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get()
        self.assertNotEquals(user.first_name, data["first_name"])



class TestUserDelete(APITestCase):
    """
    Tests Delete /users/pk:uuid
    """

    def setUp(self):
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.user_admin = UserFactory(is_superuser=True)
        self.url = reverse("user-detail", kwargs={"pk": self.user_1.pk})

    def test_valid_delete_request_from_user_deletes_user(self):
        refresh = RefreshToken.for_user(self.user_1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer  {refresh.access_token}")
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username=self.user_1.username).exists())

    def test_valid_delete_request_from_different_user_deletes_user(self):
        refresh = RefreshToken.for_user(self.user_2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer  {refresh.access_token}")
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(username=self.user_1.username).exists())

    def test_valid_delete_request_from_superuser_deletes_user(self):
        refresh = RefreshToken.for_user(self.user_admin)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer  {refresh.access_token}")
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username=self.user_1.username).exists())

    def test_unauthorized_delete_request_from_user_has_correct_responses(self):
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer fake")
        response = self.client.delete(self.url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
