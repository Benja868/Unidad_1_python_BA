from django.shortcuts import render
from dispositivos.models import Dispositivo

def index(request):
    return render(request, "index.html")

def panel(request):
    dispositivos = Dispositivo.objects.all()
    contexto = {"dispositivos": dispositivos}
    return render(request, "panel.html", contexto)

# Create your views here.
