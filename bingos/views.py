from datetime import datetime, timedelta
from django.shortcuts import render
from bingos.models import Carton, Bingo, Visita
#from requests import get
from publicidad.models import publicidad

def get_ip(): #obtiene IP
    try:
        ip_coded = get('https://api.ipify.org') #obtengo la ip codificada
        ip = ip_coded.content.decode() #la decodifico
    except:
        ip = 'No se obtuvo IP'

    return ip

def banIP(ip, fyh_visita):#es una función, no una vista
    ahora = datetime.now()+timedelta(minutes=3) #tomo la hora actual + x minutos
    diff = ahora-datetime.now() #tomo sólo hora actual
    
    if ahora > datetime.now(): #ya pasó el ban
        print('se pasó')
    else:
        print('todavía falta') #no pasó el ban todavía

    return diff

def banned():
    return

# def home(request):

#     bingos = Bingo.objects.all().filter(activo=True, fecha_sorteo__gte = datetime.now().strftime('%Y-%m-%d')).order_by('fecha_sorteo')
#     #obtener todos los bingos
#     ip = get_ip() #obtengo IP
#     #verifico si entró a la página antes
#     visita = Visita()
#     visita.idVisita = Visita.objects.all().__len__()+1 #cuento la cantidad de id y le sumo 1
#     visita.fyh_visita=datetime.now() #
#     visita.ip = ip
#     visita.save()

#     #print(banIP(visita.ip,  datetime.now()-timedelta(minutes=3)))
#     pubs = publicidad.objects.all().filter(activo=True).order_by('empresa')
#     ctx = {'bingos':bingos, 'visita':visita, 'pubs': pubs}

#     return render(request, 'control/index.html', ctx)

def buscar(request):
    bingos = Bingo.objects.all().filter(activo=True, fecha_sorteo__gte = datetime.now().strftime('%Y-%m-%d'), ).order_by('fecha_sorteo')
    pubs = publicidad.objects.all().filter(activo=True).order_by('empresa')
    ctx = {'bingos':bingos, 'pubs': pubs}

    if request.POST.get('txtCarton') == None:#si aún no se hizo submit
        return render(request, 'control/index.html', ctx)
        
    else:#si se hizo submit
        if request.POST:
            c = request.POST['txtCarton']
            idbingo=request.POST['idBingo']
            bingo = Bingo.objects.all().get(idBingo=idbingo)
            carton = Carton.objects.filter(num_carton=c, idBingo=idbingo)
            bingo.contador_consultas = bingo.contador_consultas+1
            bingo.save()
            pubs = publicidad.objects.all().filter(activo=True).order_by('empresa')
        ctx = {'carton': carton, 'bingo':bingo, 'pubs':pubs}
        return render(request, 'control/busqueda.html', ctx)

# def ip(request):

#     print(request.POST)
#     return render(request, 'ip.html')
