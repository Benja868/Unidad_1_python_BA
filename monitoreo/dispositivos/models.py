from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Zona(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Dispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    consumo = models.IntegerField()
    categoria = models.CharField(max_length=50, default="General")
    zona = models.CharField(max_length=50, default="Sin zona")

    def __str__(self):
        return self.nombre


class Medicion(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    consumo = models.IntegerField()

    def __str__(self):
        return f"{self.dispositivo.nombre} - {self.consumo}W ({self.fecha})"


class Alerta(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerta: {self.dispositivo.nombre} - {self.mensaje[:20]}..."
