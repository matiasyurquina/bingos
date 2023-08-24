#from trace import Trace
from django.db import models
#from bingos.models import Carton

class Bingo(models.Model):
    idBingo=models.PositiveIntegerField(primary_key=True)
    cantidad_cartones=models.PositiveIntegerField()
    fecha_sorteo=models.DateField(null=False)
    contador_consultas=models.PositiveIntegerField()
    nombre_bingo=models.CharField(max_length=128, null=False, unique=True)
    activo=models.BooleanField(default=True)

class Carton(models.Model):
    idCarton=models.PositiveIntegerField(primary_key=True, auto_created=True)
    idBingo=models.ForeignKey(Bingo, on_delete=models.CASCADE)
    num_carton=models.PositiveIntegerField()
    vendido=models.BooleanField(default=True)

class Visita(models.Model):
    idVisita = models.PositiveIntegerField(primary_key=True)
    fyh_visita = models.DateTimeField()
    ip = models.CharField(max_length=20)
    

