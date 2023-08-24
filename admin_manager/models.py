from django.db import models

class admin(models.Model):
    user = models.CharField(null=False, max_length=64)
    password = models.CharField(null=False, max_length=256)
    last_session = models.DateTimeField(null=False)
    active= models.BooleanField(null=False, default=True)

class TextFile(models.Model):
    file = models.FileField(null=False, max_length=128)
    