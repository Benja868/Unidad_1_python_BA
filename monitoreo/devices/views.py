from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db.models import Count, Sum   # 👈 agregado Sum
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .models import Measurement, Zone, Device, Alert, Category, UserProfile
from .models import Category, Zone


# Página de inicio
def index(request):
    return render(request, "devices/index.html")


# CREAR DISPOSITIVO
@login_required(login_url='login')
def create_device(request):
    user_profile = request.user.userprofile
    organization = user_profile.organization

    categories = Category.objects.filter(organization=organization)
    zones = Zone.objects.filter(organization=organization)

    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        consumption = request.POST.get("consumption")
        category_id = request.POST.get("category")
        zone_id = request.POST.get("zone")
        status = request.POST.get("status") == "on"

        try:
            category = Category.objects.get(id=category_id) if category_id else None
        except Category.DoesNotExist:
            category = None

        try:
            zone = Zone.objects.get(id=zone_id) if zone_id else None
        except Zone.DoesNotExist:
            zone = None

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
@login_required(login_url='login')
def edit_device(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    user_profile = request.user.userprofile
    organization = user_profile.organization

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
@login_required(login_url='login')
def dashboard(request):
    user_org = request.user.userprofile.organization

    # 🔍 búsqueda por nombre de dispositivo
    search_query = request.GET.get("search", "")

    # 📊 mediciones filtradas por organización
    measurements = Measurement.objects.filter(device__organization=user_org)

    if search_query:
        measurements = measurements.filter(device__name__icontains=search_query)

    # 📑 ordenamiento (por defecto fecha descendente)
    order = request.GET.get("order", "-timestamp")
    measurements = measurements.order_by(order)[:10]

    # zonas con conteo de dispositivos
    zones = Zone.objects.filter(organization=user_org).annotate(device_count=Count("device"))

    # alertas de la última semana
    last_week = timezone.now() - timedelta(days=7)
    alerts = Alert.objects.filter(timestamp__gte=last_week, device__organization=user_org)

    # consumo total de la organización
    total_consumption = Measurement.objects.filter(
        device__organization=user_org
    ).aggregate(total=Sum("value"))["total"] or 0

    alerts_summary = {
        "Grave": alerts.filter(severity="Grave").count(),
        "Alta": alerts.filter(severity="Alta").count(),
        "Media": alerts.filter(severity="Media").count(),
    }

    return render(request, "devices/dashboard.html", {
        "latest_measurements": measurements,
        "zones": zones,
        "alerts_summary": alerts_summary,
        "total_consumption": total_consumption,
        "search_query": search_query,
        "order": order,
    })


# LISTA DE DISPOSITIVOS
@login_required(login_url='login')
def device_list(request):
    user_org = request.user.userprofile.organization
    category_id = request.GET.get("category")
    devices = Device.objects.filter(organization=user_org)
    if category_id:
        devices = devices.filter(category_id=category_id)
    categories = Category.objects.filter(organization=user_org)
    return render(request, "devices/device_list.html", {"devices": devices, "categories": categories})


# DETALLE DE DISPOSITIVO
@login_required(login_url='login')
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
@login_required(login_url='login')
def delete_device(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    if request.method == "POST":
        device.delete()
        return redirect("device_list")
    return render(request, "devices/delete.html", {"device": device})


# LISTA DE MEDICIONES
@login_required(login_url='login')
def measurement_list(request):
    user_org = request.user.userprofile.organization
    measurements = Measurement.objects.filter(device__organization=user_org).order_by("-timestamp")
    return render(request, "devices/measurement_list.html", {"measurements": measurements})

@login_required(login_url='login')
def create_category(request):
    user_org = request.user.userprofile.organization
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name, organization=user_org)
            return redirect("create_device")  # vuelve a crear dispositivo
    return render(request, "devices/create_category.html")

@login_required(login_url='login')
def create_zone(request):
    user_org = request.user.userprofile.organization
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Zone.objects.create(name=name, organization=user_org)
            return redirect("create_device")  # vuelve a crear dispositivo
    return render(request, "devices/create_zone.html")