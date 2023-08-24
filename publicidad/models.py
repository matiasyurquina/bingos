from django.db import models

class publicidad(models.Model):

	empresa = models.CharField(max_length=128, null=False, unique=True)
	descripcion = models.CharField(max_length=256, null=False)
	tel = models.CharField(max_length=10, null=False)
	imagen = models.ImageField(null=False, max_length=256)
	link = models.CharField(max_length=256, null=False)
	activo = models.BooleanField(default=False)
	

	

