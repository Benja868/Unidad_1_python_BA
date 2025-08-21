from django.shortcuts import render

# Datos simulados de dispositivos
dispositivos = [
    {"id": 1, "nombre": "Refrigerador", "consumo": 450, "limite": 500},
    {"id": 2, "nombre": "Aire Acondicionado", "consumo": 1200, "limite": 1000},
    {"id": 3, "nombre": "Computadora", "consumo": 300, "limite": 400},
    {"id": 4, "nombre": "Televisor", "consumo": 600, "limite": 700},
]

def index(request):
    return render(request, "index.html")

def panel(request):
    contexto = {"dispositivos": dispositivos}
    return render(request, "panel.html", contexto)

# Create your views here.
