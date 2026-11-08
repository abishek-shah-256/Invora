from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .models import Role, Department, AuditLog
from .forms import LoginForm, UserCreateForm, UserUpdateForm, AdminSetPasswordForm, ProfileForm, RoleForm, DepartmentForm
from .decorators import admin_required
from .utils import log_action

User = get_user_model()


class InvoraLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request, "LOGIN", "User", self.request.user.pk, "User signed in.")
        return response


class InvoraLogoutView(LogoutView):
    http_method_names = ["post", "options"]


@login_required
def dashboard(request):
    recent_logs = AuditLog.objects.select_related("actor")[:8]
    context = {
        "total_users": User.objects.count(),
        "active_users": User.objects.filter(is_active=True).count(),
        "inactive_users": User.objects.filter(is_active=False).count(),
        "total_roles": Role.objects.count(),
        "total_departments": Department.objects.count(),
        "recent_logs": recent_logs,
        "role_counts": [
            {"name": role.name, "count": role.users.count()} for role in Role.objects.all()
        ],
    }
    return render(request, "accounts/dashboard.html", context)


@login_required
@admin_required
def user_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    role = request.GET.get("role", "")
    users = User.objects.select_related("role", "department")
    if query:
        users = users.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(email__icontains=query) | Q(employee_id__icontains=query)
        )
    if status == "active":
        users = users.filter(is_active=True)
    elif status == "inactive":
        users = users.filter(is_active=False)
    if role:
        users = users.filter(role__code=role)
    return render(request, "accounts/users/list.html", {
        "users": users, "query": query, "status": status, "selected_role": role,
        "roles": Role.objects.all(),
    })


@login_required
@admin_required
def user_create(request):
    form = UserCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        log_action(request, "CREATE", "User", user.pk, f"Created user {user.email}.")
        messages.success(request, f"{user.get_full_name()} was created successfully.")
        return redirect("user_detail", pk=user.pk)
    return render(request, "accounts/form.html", {"form": form, "title": "Add user", "subtitle": "Create a new Invora account", "cancel_url": "user_list"})


@login_required
@admin_required
def user_detail(request, pk):
    user_obj = get_object_or_404(User.objects.select_related("role", "department"), pk=pk)
    logs = AuditLog.objects.filter(entity_type="User", entity_id=str(user_obj.pk))[:10]
    return render(request, "accounts/users/detail.html", {"user_obj": user_obj, "logs": logs})


@login_required
@admin_required
def user_update(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    form = UserUpdateForm(request.POST or None, instance=user_obj)
    if request.method == "POST" and form.is_valid():
        updated = form.save()
        log_action(request, "UPDATE", "User", updated.pk, f"Updated user {updated.email}.")
        messages.success(request, "User details updated.")
        return redirect("user_detail", pk=updated.pk)
    return render(request, "accounts/form.html", {"form": form, "title": "Edit user", "subtitle": user_obj.email, "cancel_url": "user_detail", "cancel_pk": pk})


@login_required
@admin_required
@require_POST
def user_toggle_status(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if user_obj.pk == request.user.pk:
        messages.error(request, "You cannot deactivate your own account.")
    elif user_obj.is_superuser and not request.user.is_superuser:
        messages.error(request, "Only a superuser can change another superuser's status.")
    else:
        user_obj.is_active = not user_obj.is_active
        user_obj.save(update_fields=["is_active"])
        action = "ACTIVATE" if user_obj.is_active else "DEACTIVATE"
        log_action(request, action, "User", user_obj.pk, f"{user_obj.email} was {action.lower()}d.")
        messages.success(request, f"User account {action.lower()}d.")
    return redirect("user_detail", pk=pk)


@login_required
@admin_required
def user_set_password(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    form = AdminSetPasswordForm(user_obj, request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_action(request, "PASSWORD_RESET", "User", user_obj.pk, f"Administrator reset password for {user_obj.email}.")
        messages.success(request, "Password updated successfully.")
        return redirect("user_detail", pk=pk)
    return render(request, "accounts/form.html", {"form": form, "title": "Set user password", "subtitle": user_obj.email, "cancel_url": "user_detail", "cancel_pk": pk})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        log_action(request, "UPDATE_PROFILE", "User", request.user.pk, "User updated their profile.")
        messages.success(request, "Your profile was updated.")
        return redirect("profile")
    return render(request, "accounts/form.html", {"form": form, "title": "My profile", "subtitle": "Update your personal details", "cancel_url": "dashboard"})


class InvoraPasswordChangeView(PasswordChangeView):
    template_name = "accounts/form.html"
    success_url = reverse_lazy("profile")
    extra_context = {"title": "Change password", "subtitle": "Choose a strong password", "cancel_url": "profile"}

    def form_valid(self, form):
        messages.success(self.request, "Your password was changed.")
        log_action(self.request, "CHANGE_PASSWORD", "User", self.request.user.pk, "User changed their password.")
        return super().form_valid(form)


@login_required
@admin_required
def role_list(request):
    return render(request, "accounts/roles/list.html", {"roles": Role.objects.all()})


@login_required
@admin_required
def role_create(request):
    form = RoleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        role = form.save()
        log_action(request, "CREATE", "Role", role.pk, f"Created role {role.name}.")
        messages.success(request, "Role created.")
        return redirect("role_list")
    return render(request, "accounts/form.html", {"form": form, "title": "Add role", "subtitle": "Define a role and its permission keys", "cancel_url": "role_list"})


@login_required
@admin_required
def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if role.is_system and request.method == "POST":
        messages.error(request, "System roles cannot be edited in this first release.")
        return redirect("role_list")
    form = RoleForm(request.POST or None, instance=role)
    if request.method == "POST" and form.is_valid():
        role = form.save()
        log_action(request, "UPDATE", "Role", role.pk, f"Updated role {role.name}.")
        messages.success(request, "Role updated.")
        return redirect("role_list")
    return render(request, "accounts/form.html", {"form": form, "title": "Edit role", "subtitle": role.name, "cancel_url": "role_list", "readonly": role.is_system})


@login_required
@admin_required
def department_list(request):
    return render(request, "accounts/departments/list.html", {"departments": Department.objects.all()})


@login_required
@admin_required
def department_create(request):
    form = DepartmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        department = form.save()
        log_action(request, "CREATE", "Department", department.pk, f"Created department {department.name}.")
        messages.success(request, "Department created.")
        return redirect("department_list")
    return render(request, "accounts/form.html", {"form": form, "title": "Add department", "subtitle": "Create an organisational department", "cancel_url": "department_list"})


@login_required
@admin_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    form = DepartmentForm(request.POST or None, instance=department)
    if request.method == "POST" and form.is_valid():
        department = form.save()
        log_action(request, "UPDATE", "Department", department.pk, f"Updated department {department.name}.")
        messages.success(request, "Department updated.")
        return redirect("department_list")
    return render(request, "accounts/form.html", {"form": form, "title": "Edit department", "subtitle": department.name, "cancel_url": "department_list"})


@login_required
@admin_required
def audit_list(request):
    logs = AuditLog.objects.select_related("actor")
    query = request.GET.get("q", "").strip()
    if query:
        logs = logs.filter(Q(action__icontains=query) | Q(entity_type__icontains=query) | Q(description__icontains=query) | Q(actor__email__icontains=query))
    return render(request, "accounts/audit/list.html", {"logs": logs[:200], "query": query})
