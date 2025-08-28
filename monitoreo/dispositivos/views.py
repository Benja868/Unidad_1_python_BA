from django.shortcuts import render
from dispositivos.models import Dispositivo
from .models import Dispositivo

def index(request):
    return render(request, "index.html")

def panel(request):
    dispositivos = Dispositivo.objects.all()
    contexto = {"dispositivos": dispositivos}
    return render(request, "dispositivos/panel.html", contexto)

def inicio(request):
    # dispositivos = Dispositivo.objects.all()
    dispositivos = Dispositivo.objects.select_related("categoria") # join

def dispositivo(request, dispositivo_id):
    dispositivo = Dispositivo.objects.get(id=dispositivo_id)
    return render(request, "dispositivos/dispositivo.html", {"dispositivo": dispositivo})

# Create your views here.