from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Role, Department

class UserManagementTests(TestCase):
    def setUp(self):
        self.admin_role = Role.objects.create(name="Administrator", code="admin", is_system=True)
        self.staff_role = Role.objects.create(name="Department Staff", code="department-staff")
        self.department = Department.objects.create(name="Operations", code="OPS")
        self.admin = User.objects.create_superuser(
            email="admin@invora.test", password="StrongPass123!",
            first_name="Invora", last_name="Admin", role=self.admin_role
        )
        self.client = Client()

    def test_password_is_hashed(self):
        user = User.objects.create_user(email="staff@invora.test", password="StrongPass123!", first_name="Test", last_name="Staff")
        self.assertNotEqual(user.password, "StrongPass123!")
        self.assertTrue(user.check_password("StrongPass123!"))

    def test_admin_can_open_user_management(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_open_user_management(self):
        staff = User.objects.create_user(email="staff@invora.test", password="StrongPass123!", first_name="Test", last_name="Staff", role=self.staff_role)
        self.client.force_login(staff)
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 403)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
