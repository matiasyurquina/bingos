from django.shortcuts import render
from publicidad.models import publicidad

def slider(request):
    pubs = publicidad.objects.all().filter(activo=True)
    ctx={'pubs': pubs}
    return render(request, "publicidad/slider.html", ctx)