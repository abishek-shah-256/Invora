# Invora – Week 1: User Management System

A working Django user-management foundation for the Invora Online Inventory and Procurement Management System.

## Week 1 features

- Email-and-password login and logout
- Custom user model with BCrypt-SHA256 password hashing
- Six baseline system roles
- Department management
- User create, list, search, filter, view and edit
- Activate/deactivate user accounts
- Administrator password reset
- User profile and password change
- Server-side administrator access checks
- Audit trail for login and user/role/department administration events
- Responsive dashboard and Bootstrap-based UI
- SQLite by default; PostgreSQL configuration supported

## Technology note

The Capstone Project 1 report specified DJANGO Python and PostgreSQL. This implementation follows the team's later decision to use Django. Confirm this stack change with the lecturer/client and update project documentation if required.

## Requirements

- Python 3.10+
- pip

## Run locally (Windows PowerShell)

```powershell
# 1. Extract the ZIP and open the project folder
cd invora_week1_user_management

# 2. Create and activate a virtual environment
py -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create local environment file
Copy-Item .env.example .env

# 5. Create database tables
python manage.py makemigrations accounts
python manage.py migrate

# 6. Create Invora's six baseline roles
python manage.py setup_invora

# 7. Create the first administrator account
python manage.py createsuperuser

# 8. Start the development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in using the superuser email and password.

> The first administrator created with `createsuperuser` can administer Invora even if no role is assigned. To show the Administrator role beside the account, edit the user in Django Admin at `/django-admin/` and assign the `Administrator` role.

## PostgreSQL configuration

Create a PostgreSQL database, then update `.env`:

```env
DB_ENGINE=postgresql
DB_NAME=invora
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

Run migrations after changing the database configuration.

## Important URLs

| URL | Purpose |
|---|---|
| `/login/` | Sign in |
| `/` | Dashboard |
| `/users/` | User management |
| `/users/add/` | Create user |
| `/roles/` | Roles |
| `/departments/` | Departments |
| `/audit-logs/` | Audit history |
| `/profile/` | My profile |
| `/django-admin/` | Django administration |

## Baseline roles

The `setup_invora` command creates:

1. Administrator
2. Department Staff
3. Approver
4. Procurement Officer
5. Inventory Officer
6. Finance Officer

Custom roles can be added from the Roles & Permissions page. The permissions JSON field stores permission keys for use by later modules. Actual access to each future module must be enforced in its Django views/API, not only hidden in the interface.

## Team split suggestion for Week 1

- Abishek: project setup, custom user model, authentication and integration
- Pratikshya: user create/edit forms and validation
- Roshan: roles, departments and permission design
- Bhabita: dashboard, templates and responsive UI
- Ashish: testing, audit-log verification and setup documentation

Review and test each other's work before merging.

## Security and development notes

- Django CSRF protection is enabled on forms.
- User-management views enforce administrator access on the server.
- Passwords are stored as hashes, never as plain text.
- AuditLog entries are append-only through the model and read-only in Django Admin.
- Do not use the development secret key or `DEBUG=True` in production.
- Before production, configure HTTPS, secure cookies, email-based password reset, backups, monitoring, and a proper deployment environment.
- This is the Week 1 foundation. Procurement/inventory-specific permission enforcement and API security will be expanded with those modules.
