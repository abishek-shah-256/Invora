from django.core.management.base import BaseCommand
from accounts.models import Role

SYSTEM_ROLES = [
    ("Administrator", "admin", "Full access to user, role and department administration."),
    ("Department Staff", "department-staff", "Submit and track purchase requests for their department."),
    ("Approver", "approver", "Review, approve, reject or request information on purchase requests."),
    ("Procurement Officer", "procurement-officer", "Manage quotations, suppliers and purchase orders."),
    ("Inventory Officer", "inventory-officer", "Manage item catalogue, stock levels and stock transactions."),
    ("Finance Officer", "finance-officer", "Manage invoices, payments and finance reports."),
]

class Command(BaseCommand):
    help = "Create Invora's six baseline system roles."

    def handle(self, *args, **options):
        for name, code, description in SYSTEM_ROLES:
            role, created = Role.objects.get_or_create(
                code=code,
                defaults={"name": name, "description": description, "is_system": True},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created role: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")
        self.stdout.write(self.style.SUCCESS("Invora baseline roles are ready."))
