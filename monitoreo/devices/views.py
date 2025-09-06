from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .models import Measurement, Zone, Device, Alert, Category, UserProfile


# Página de inicio
def index(request):
    return render(request, "devices/index.html")


# CREAR DISPOSITIVO
def create_device(request):
    user_profile = request.user.userprofile
    organization = user_profile.organization

    # Filtramos categorías y zonas por la organización del usuario
    categories = Category.objects.filter(organization=organization)
    zones = Zone.objects.filter(organization=organization)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        consumption = request.POST.get("consumption")
        category_id = request.POST.get("category")
        zone_id = request.POST.get("zone")
        status = request.POST.get("status") == "on"

        # Manejo seguro de objetos relacionados
        try:
            category = Category.objects.get(id=category_id) if category_id else None
        except Category.DoesNotExist:
            category = None

        try:
            zone = Zone.objects.get(id=zone_id) if zone_id else None
        except Zone.DoesNotExist:
            zone = None

        # Creamos el dispositivo asociado a la organización del usuario
        Device.objects.create(
            name=name,
            description=description,
            consumption=consumption,
            category=category,
            zone=zone,
            status=status,
            organization=organization
        )
        return redirect("device_list")

    return render(request, "devices/create_device.html", {
        "categories": categories,
        "zones": zones
    })

# EDITAR DISPOSITIVO
def edit_device(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    user_profile = request.user.userprofile
    organization = user_profile.organization

    # Filtrar categorías y zonas por la organización del usuario
    categories = Category.objects.filter(organization=organization)
    zones = Zone.objects.filter(organization=organization)

    if request.method == "POST":
        device.name = request.POST.get("name")
        device.description = request.POST.get("description")
        device.consumption = request.POST.get("consumption")
        device.status = request.POST.get("status") == "on"

        category_id = request.POST.get("category")
        zone_id = request.POST.get("zone")

        device.category = Category.objects.get(id=category_id) if category_id else None
        device.zone = Zone.objects.get(id=zone_id) if zone_id else None

        device.save()
        return redirect("device_list")

    return render(request, "devices/edit_device.html", {
        "device": device,
        "categories": categories,
        "zones": zones
    })


# LOGIN
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "devices/login.html", {"error": "Credenciales inválidas"})
    return render(request, "devices/login.html")


# REGISTRO
def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "devices/register.html", {"error": "El usuario ya existe"})
    return render(request, "devices/register.html")


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect("login")


# RECUPERAR CONTRASEÑA (solo maqueta)
def recover_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        return render(request, "devices/recover.html", {"message": f"Se ha enviado un correo a {email} (maqueta)"})
    return render(request, "devices/recover.html")


# DASHBOARD
def dashboard(request):
    latest_measurements = Measurement.objects.order_by("-timestamp")[:10]
    user_org = request.user.userprofile.organization
    zones = Zone.objects.filter(organization=user_org).annotate(device_count=Count("device"))
    last_week = timezone.now() - timedelta(days=7)
    alerts = Alert.objects.filter(timestamp__gte=last_week, device__organization=user_org)
    alerts_summary = {
        "Grave": alerts.filter(severity="Grave").count(),
        "Alta": alerts.filter(severity="Alta").count(),
        "Media": alerts.filter(severity="Media").count(),
    }
    return render(request, "devices/dashboard.html", {
        "latest_measurements": latest_measurements,
        "zones": zones,
        "alerts_summary": alerts_summary,
    })


# LISTA DE DISPOSITIVOS
def device_list(request):
    user_org = request.user.userprofile.organization
    category_id = request.GET.get("category")
    devices = Device.objects.filter(organization=user_org)
    if category_id:
        devices = devices.filter(category_id=category_id)
    categories = Category.objects.filter(organization=user_org)
    return render(request, "devices/device_list.html", {"devices": devices, "categories": categories})


# DETALLE DE DISPOSITIVO
def device_detail(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    measurements = Measurement.objects.filter(device=device).order_by("-timestamp")
    alerts = Alert.objects.filter(device=device).order_by("-timestamp")
    return render(request, "devices/device_detail.html", {
        "device": device,
        "measurements": measurements,
        "alerts": alerts
    })


# ELIMINAR DISPOSITIVO
def delete_device(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    if request.method == "POST":
        device.delete()
        return redirect("device_list")
    return render(request, "devices/delete.html", {"device": device})


# LISTA DE MEDICIONES
def measurement_list(request):
    measurements = Measurement.objects.all().order_by("-timestamp")
    return render(request, "devices/measurement_list.html", {"measurements": measurements})
