# Invora Week 2 — Inventory Management

This package **extends your uploaded Week 1 Django application**. Existing `accounts` code and migration are retained. The new `inventory` Django app introduces Category, Unit and InventoryItem.

## Windows PowerShell setup

1. Extract this ZIP to a **new folder**, then open PowerShell in the folder containing `manage.py`.
2. If necessary, create and activate a virtual environment:
   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install packages:
   ```powershell
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and enter your **own PostgreSQL connection details**. The uploaded project used port `5433`; retain it if your PostgreSQL instance still uses that port.
5. Apply migrations **before** initialising roles:
   ```powershell
   python manage.py migrate
   python manage.py setup_invora
   ```
   If this is a new database, also create an administrator with `python manage.py createsuperuser`.
6. Start the server:
   ```powershell
   python manage.py runserver
   ```
7. Visit `http://127.0.0.1:8000/inventory/` after logging in.

## Permissions

- Any authenticated user can view inventory, categories, units and low-stock indicators.
- Administrators and users with the `inventory-officer` role code can create/edit inventory items, categories and units, and activate/deactivate items.
- Inventory edits are written to the existing AuditLog model.

## Important scope note

Week 2 stores **opening stock quantity** on items. It does **not** yet implement inward/outward stock transactions or a stock ledger. Those belong to Week 3. No sample inventory records are automatically inserted.

## Security note

The Week 1 ZIP contained a plaintext PostgreSQL password in `invora/settings.py`. This package removes that hard-coded password and reads the database credentials from `.env` instead. Since the old password was exposed in the ZIP, change it in PostgreSQL and update your local `.env`. Do not commit `.env` to GitHub.
