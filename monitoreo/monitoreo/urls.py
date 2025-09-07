from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from devices import views  # usamos solo views de la app devices

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Redirigir la raíz al dashboard
    path("", RedirectView.as_view(url="/dashboard/")),

    # Auth (login, logout, registro, recuperación)
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path("recover/", views.recover_password, name="recover"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # App devices
    path("", include("devices.urls")),  # incluye todas las rutas de devices
]
