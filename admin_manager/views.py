from django.shortcuts import render, redirect
from publicidad.models import publicidad
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from bingos.models import Bingo, Carton
from django.db.utils import IntegrityError, InternalError
from django.core.paginator import Paginator
from .forms import TextFileForm
import re
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required

def ListarBingos()-> Bingo:
    return Bingo.objects.all().filter(activo=True).order_by('fecha_sorteo', 'nombre_bingo')
    #Bingo.objects.all().filter(activo=True).order_by('fecha_sorteo', 'nombre_bingo')

def getBingo(id)-> Bingo:
    try:
        result = Bingo.objects.get(idBingo=id)
    except:
        result = None
    
    return result

def httpsFunc(cad):
    cad.strip(" ")
    https = r'https?://\S+'
    url = re.findall(https, cad)

    if url.__len__()!=0:#si encuentro https
        return cad 
    else: #si no se encuentra nada
        return "https://"+cad

def saveReg(reg): 

    try:
        reg.save()
        result = 0
        return result
    except IntegrityError:
        result = 1
        return result

    except:
        result = 2
        return result
    
def multiSaveCarton(cartones, idBingo, cant_cart):
    idCarton = Carton.objects.count()+1
    cont=0
    result = 0
    
    for i in range(cant_cart):
            cartones.idCarton = idCarton
            cartones.num_carton = i+1
            cartones.vendido = False
            idCarton+=1
            cartones.idBingo = idBingo
            idCarton+=1
            cont+=1

            try:
                cartones.save()
            except:
                result = 1
                return result
    
    return result


def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_home')  # Cambia esto a la página que desees después del login
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'admin_manager/base_admin.html')

def publicidad_view(request):
    return render(request, 'admin_manager/publicidad/menu_publicidad.html')

def pub_crear(request):
    
    if request.POST:
        
        if request.FILES.get('imagen'):
            img = request.FILES['imagen']
            fs = FileSystemStorage()
            img_bd = settings.MEDIA_ROOT + "/images/"+ img.name
            filename = fs.save(img_bd, img)
            uploaded_file_url = fs.url(filename)

            pub = publicidad()
            pub.empresa = request.POST['empresa']
            pub.descripcion = request.POST['descripcion']
            pub.tel = request.POST['tel']
            pub.imagen = "/media/images/"+img.name
            pub.link =  httpsFunc(request.POST['link'])
            pub.activo = request.POST['activo']
            res = saveReg(pub)
            if res == 0:
                msg = 'La publicidad se creó correctamente'
            elif res == 1:
                msg='Ya existe una publicidad con el nombre: '+request.POST['empresa']
                return render(request, 'admin_manager/publicidad/error.html', {'msg':msg})
            else:
                msg='Ocurrió un error inesperado, contáctese con su desarrollador'
                return render(request, 'admin_manager/publicidad/error.html', {'msg':msg})

        return render(request, 'admin_manager/publicidad/editarSuccess.html', {'uploaded_file_url': uploaded_file_url, 'msg': msg})
    else:
        return render(request, 'admin_manager/publicidad/nueva.html')

def pub_editar(request, id):#muestra las publicidades existentes

    pub = publicidad.objects.get(pk=id)
    
    if request.POST:

        pub.empresa = request.POST['empresa'].strip(" ")
        pub.descripcion = request.POST['descripcion'].strip(" ")
        pub.tel = request.POST['tel']
        pub.link = httpsFunc(request.POST['link'])
        pub.activo = request.POST['activo']
            
        if request.FILES.get('imagen')!=None:#se eleigió una imagen
            img = request.FILES['imagen']
            fs = FileSystemStorage()
            img_bd = settings.MEDIA_ROOT + "/images/"+ img.name
            filename = fs.save(img_bd, img)
            uploaded_file_url = fs.url(filename)
            pub.imagen = "/media/images/"+img.name
            res = saveReg(pub)

            if res == 0:
                msg = 'La publicidad se editó correctamente'
                return render(request, 'admin_manager/publicidad/editarSuccess.html', {'uploaded_file_url': uploaded_file_url, 'msg':msg})

            elif res == 1:
                msg='Ya existe una publicidad con el nombre: '+request.POST['empresa']
                return render(request, 'admin_manager/publicidad/error.html', {'msg':msg})
            else:
                msg='Ocurrió un error inesperado, contáctese con su desarrollador'
                return render(request, 'admin_manager/publicidad/error.html', {'msg':msg})

        else:#NO se eleigió una imagen
            res = saveReg(pub)
            if res == 0:
                msg = 'La publicidad se editó correctamente'
                return render(request, 'admin_manager/publicidad/editarSuccess.html', {'msg':msg})
            elif res == 1:
                msg='Ya existe una publicidad con el nombre: '+request.POST['empresa']
                return render(request, 'admin_manager/publicidad/error.html', {'msg':msg})
            else:
                msg='Ocurrió un error inesperado, contáctese con su desarrollador'
                return render(request, 'admin_manager/publicidad/error.html', {'msg':msg})
    else:
        return render(request, 'admin_manager/publicidad/editar.html', {'pub':pub})
    

def pub_editarShow(request):#muestra las publicidades existentes
    pubs = publicidad.objects.all().order_by('-activo', 'empresa')
    
    return render(request, 'admin_manager/publicidad/editar.html', {'pubs':pubs})


def bingos_menu(request):
    return render(request, 'admin_manager/bingos/menu_bingos.html')

def bingos_nuevo(request):
    
    if request.POST:
        bingo = Bingo()
        bingo.idBingo = Bingo.objects.count()+1
        bingo.cantidad_cartones = request.POST['cantidad_bingos']
        bingo.nombre_bingo = request.POST['nombre_bingo']
        bingo.fecha_sorteo = request.POST['fecha_sorteo']
        bingo.activo = True
        bingo.contador_consultas = 0

        res = saveReg(bingo)
        if res == 0:
            msg = 'El bingo '+ request.POST['nombre_bingo'] + ' se guardó correctamente'
        elif res == 1:
            msg='Ya existe un bingo con el nombre: '+request.POST['nombre_bingo']
            return render(request, 'admin_manager/bingos/error.html', {'bingos':bingo, 'msg':msg})
        else:
            msg='Ocurrió un error con la conexión a la base de datos'
            return render(request, 'admin_manager/bingos/error.html', {'bingos':bingo, 'msg':msg})

        cartones = Carton()
        idBingo = Bingo(bingo.idBingo)

        res = multiSaveCarton(cartones, idBingo, int(bingo.cantidad_cartones))

        if res == 0:
            msg=f"El bingo {request.POST['nombre_bingo']} se creó correctamente"
            return render(request, 'admin_manager/bingos/nuevoSuccess.html', {'msg': msg}) 
        else:
            msg='Ocurrió un error con inesperado, contáctese con su administrador'
            bingo.delete()
        return render(request, 'admin_manager/bingos/error.html', {'bingos':bingo, 'msg':msg})
        
    else:
        return render(request, 'admin_manager/bingos/nuevo.html')

def bingos_editarShow(request):

    if request.POST:
        return render(request, 'admin_manager/bingos/editar_show.html')
    else:
        bingos = ListarBingos()
        return render(request, 'admin_manager/bingos/editar_show.html', {'bingos':bingos})

def bingos_editar(request, id):

    if request.POST:#Si se hace submit
        bingo = getBingo(id)

        if bingo == None:
            msg = 'El bingo indicado no existe'
            return render(request, 'admin_manager/bingos/error.html', {'msg': msg})

        bingo.nombre_bingo = request.POST['nombre_bingo']
        cantidad_vieja = bingo.cantidad_cartones
        bingo.fecha_sorteo = request.POST['fecha_sorteo']
        

        cartones = Carton()
        idCarton = Carton.objects.count()+1
        idBingo = Bingo(bingo.idBingo)
        cantidad_nueva = int(request.POST['cantidad_cartones'])

        if cantidad_nueva > cantidad_vieja:#Se agregan cartones

            for i in range(cantidad_vieja, cantidad_nueva):
                cartones.idCarton = idCarton
                cartones.num_carton = i+1
                cartones.vendido = False
                idCarton+=1
                cartones.idBingo = idBingo
                if saveReg(cartones)!=0:
                    msg = 'Ocurrió un error inesperado'
                    return render(request, 'admin_manager/bingos/error.html', {'msg': msg})

            bingo.cantidad_cartones = cantidad_nueva

        elif cantidad_nueva < cantidad_vieja: #Se BORRAN cartones
                cartones = Carton.objects.all().filter(num_carton__gt=cantidad_nueva, num_carton__lte=cantidad_vieja, idBingo=idBingo)
                cartones.delete()
                bingo.cantidad_cartones = cantidad_nueva

        res = saveReg(bingo)
        if res == 0:
            msg = f"Los datos se guardaron correcatemente en: {request.POST['nombre_bingo']}"
            return render(request, 'admin_manager/bingos/editarSuccess.html', {'msg': msg})
        elif res == 1:
            msg = f"Ya existe un bingo con el nombre: {request.POST['nombre_bingo']}"
            return render(request, 'admin_manager/bingos/error.html', {'msg': msg})
        else:
            msg = 'Ocurrió un error inesperado'
            return render(request, 'admin_manager/bingos/error.html', {'msg': msg})    

    else:#Si no se hace muestra solamente los datos del item seleccionado
        bingo = getBingo(id)
    return render(request, 'admin_manager/bingos/editar.html', {'bingo':bingo})


def carton_menu(request):
    return render(request, 'admin_manager/carton/cartonMenu.html')

def carton_show(request):#Muestra los bingos activos
    bingos = ListarBingos()
    return render(request, 'admin_manager/carton/verCartones.html', {'bingos': bingos})

def carton_editar(request, id):

    cartones = Carton.objects.filter(idBingo=id).order_by('num_carton')
    bingo = getBingo(id)

    if cartones.count() != 0:#si se enecuentra algo
        paginator = Paginator(cartones, 100)
        page = request.GET.get('page')
        cartones = paginator.get_page(page)
        
        return render(request, 'admin_manager/carton/editarCarton.html', {'cartones': cartones, 'bingo': bingo, 'page': page })   
    else:#Si no se encuentra nada
        return render(request, 'admin_manager/carton/editarCarton.html')
    
def carton_editarCarton(request, id, idCarton):
    
    if request.GET.get('page') != None:
        page = request.GET.get('page')
    else: 
        page = 1
    
    carton = Carton.objects.get(idCarton=idCarton)

    if request.POST:#si se hizo submit
        if carton.vendido == True:
            carton.vendido = False
        else:
            carton.vendido = True
        reg = saveReg(carton)

        if reg == 0:
            msg = 'Datos guardados'
            return render(request, 'admin_manager/carton/editarCartonSolo.html', {'id': id, 'carton': carton, 'page': page, 'msg': msg})
        else:
            msg = 'Ocurrió un error inesperado'
            return render(request, 'admin_manager/carton/editarCartonSolo.html', {'id': id, 'carton': carton, 'page': page, 'msg': msg})
    
    else:
        return render(request, 'admin_manager/carton/editarCartonSolo.html', {'id': id, 'carton': carton, 'page': page})
    
    
def carton_subir(request):#Muestra los bingos activos
    bingos = ListarBingos()

    return render(request, 'admin_manager/carton/subirCarton.html', {'bingos':bingos})


def carton_subirVer(request, id):#Muestra los bingos activos
    
    bingo = getBingo(id)
    

    if request.method == 'POST':
        form = TextFileForm(request.POST, request.FILES)
        if form.is_valid():
            text_file = form.save()

            file_content = text_file.file.read().decode('utf-8')
            lista_num= re.findall(r'\d+', file_content)#busca solamente numeros enteros
            
            cant = Carton.objects.filter(num_carton__in=lista_num, idBingo=id).update(vendido=True)
            cartones = Carton.objects.filter(num_carton__in=lista_num, idBingo=id)
            
            return render(request, 'admin_manager/carton/subirCartonVer.html', {'file_content': file_content, 'cartones': cartones, 'bingo':bingo, 'idBingo_id': id})
    else:
        form = TextFileForm()

    return render(request, 'admin_manager/carton/subirCartonVer.html', {'bingo':bingo, 'form': form})


def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)