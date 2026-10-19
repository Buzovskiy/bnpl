from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Customer


class CustomerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration_login_profile_and_logout(self):
        response = self.client.post("/api/v1/auth/register/", {
            "email": "TEST@example.com", "password": "VeryStrongTestPassw0rd!",
            "first_name": "Test",
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Customer.objects.get().email, "test@example.com")
        login = self.client.post("/api/v1/auth/login/", {
            "email": "test@example.com", "password": "VeryStrongTestPassw0rd!",
        })
        self.assertEqual(login.status_code, 200)
        self.assertIn("access", login.data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        profile = self.client.get("/api/v1/customers/me/")
        self.assertEqual(profile.status_code, 200)
        self.assertEqual(profile.data["email"], "test@example.com")
        self.assertNotIn("password", profile.data)
        logout = self.client.post("/api/v1/auth/logout/", {"refresh": login.data["refresh"]})
        self.assertEqual(logout.status_code, 204)

    def test_no_anonymous_profile_access(self):
        self.assertEqual(self.client.get("/api/v1/customers/me/").status_code, 401)

    def test_registration_cannot_set_admin_flags(self):
        response = self.client.post("/api/v1/auth/register/", {
            "email": "safe@example.com", "password": "VeryStrongTestPassw0rd!",
            "is_staff": True, "is_superuser": True,
        })
        self.assertEqual(response.status_code, 201)
        user = Customer.objects.get(email="safe@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
