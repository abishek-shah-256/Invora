from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.InvoraLoginView.as_view(), name="login"),
    path("logout/", views.InvoraLogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path("profile/password/", views.InvoraPasswordChangeView.as_view(), name="password_change"),
    path("users/", views.user_list, name="user_list"),
    path("users/add/", views.user_create, name="user_create"),
    path("users/<int:pk>/", views.user_detail, name="user_detail"),
    path("users/<int:pk>/edit/", views.user_update, name="user_update"),
    path("users/<int:pk>/status/", views.user_toggle_status, name="user_toggle_status"),
    path("users/<int:pk>/password/", views.user_set_password, name="user_set_password"),
    path("roles/", views.role_list, name="role_list"),
    path("roles/add/", views.role_create, name="role_create"),
    path("roles/<int:pk>/edit/", views.role_update, name="role_update"),
    path("departments/", views.department_list, name="department_list"),
    path("departments/add/", views.department_create, name="department_create"),
    path("departments/<int:pk>/edit/", views.department_update, name="department_update"),
    path("audit-logs/", views.audit_list, name="audit_list"),
]
