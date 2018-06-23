import os
# from requests import auth
from PIL import Image
from django.contrib import auth
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from .forms import ProfileForm, PlaceForm, PhotoForm, AddressForm, LatLonForm, FavoritosForm, VotosForm
from .models import Place, Photo, Favoritos, Votos


# -------------------------------------------------------------------------------
# VISTAS para administración
# -------------------------------------------------------------------------------
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if 'lat' in request.POST:
                lat = request.POST['lat']
                lon = request.POST['lon']
                request.session['userlatlon'] = (lat, lon)
            return redirect('user_info', pk=user.pk)
        else:
            errorlogin = '1'
            return render(request, 'login.html', {'errorlogin':errorlogin})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required
@permission_required('auth.change_user', login_url='denied')
def addtoadmin(request, pk):
    user = User.objects.get(pk=pk)
    user.groups.remove(Group.objects.get(name='usuarios'))
    user.groups.add(Group.objects.get(name='administradores'))
    user.profile.tipo = "administradores"
    return redirect('user_info', pk=pk)

@login_required
@permission_required('auth.change_user', login_url='denied')
def addtousers(request, pk):
    user = User.objects.get(pk=pk)
    user.groups.remove(Group.objects.get(name='administradores'))
    user.groups.add(Group.objects.get(name='usuarios'))
    return redirect('user_info', pk=pk)

# -------------------------------------------------------------------------------
# VISTAS para los usuarios
# -------------------------------------------------------------------------------
def new_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            item = form.save(commit=False)
            item.save()
            profile = profile_form.save(commit=False)
            profile.user = item
            profile.tipo = 'usuarios'
            profile.save()
            item.groups.add(Group.objects.get(name='usuarios'))
            auth.login(request, auth.authenticate(username=request.POST['username'], password=request.POST['password1']))
            if 'lat' in request.POST:
                lat = request.POST['lat']
                lon = request.POST['lon']
                request.session['userlatlon'] = (lat, lon)
            return redirect('user_info', pk=item.pk)
    else:
        form = UserCreationForm()
        profile_form = ProfileForm()
    return render(request, 'new_user.html', {'form': form, 'profile_form': profile_form})

@login_required
def edit_user(request, pk):
    item = User.objects.get(pk=pk)
    if item.pk == request.user.pk:
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, instance=item.profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('user_info', pk=item.pk)
        else:
            profile_form = ProfileForm(instance=item.profile)
        return render(request, 'edit_user.html', {'profile_form': profile_form})
    elif request.user.has_perm('auth.change_user'):
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, instance=item.profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('user_info', pk=item.pk)
        else:
            profile_form = ProfileForm(instance=item.profile)
        return render(request, 'edit_user.html', {'profile_form': profile_form})
    else:
        return render(request, 'denied.html')

@login_required
# @permission_required('auth.delete_user', login_url='denied')
def delete_user(request, pk):
    item = User.objects.get(pk=pk)
    if request.user.has_perm('auth.delete_user'):
        item.delete()
        item_list = User.objects.filter(is_superuser=False).order_by('username')
        request.session['mensaje'] = 'Cuenta de usuario eliminada con éxito'
        return render(request, 'user_list.html', {'item_list': item_list})
    elif item.pk == request.user.pk:
        item.delete()
        auth.logout(request)
        request.session['mensaje'] = 'Cuenta de usuario eliminada con éxito'
        return redirect('home')
    else:
        return render(request, 'denied.html')

@login_required
def user_info(request, pk):
    mensaje = ''
    if 'mensaje' in request.session:
        mensaje = request.session['mensaje']
        del request.session['mensaje']
    print(mensaje)
    item_list = Place.objects.all()
    item = get_object_or_404(User, pk=pk)
    form = UserCreationForm(instance=item)
    if item.pk == 1:
        item_list = User.objects.filter(is_superuser=False).order_by('username')
        return render(request, 'user_list.html', {'item_list': item_list, 'mensaje': mensaje})
    else:
        profile_form = ProfileForm(instance=item.profile)
        favs = Favoritos.objects.all().filter(usuario_id=pk)
        favoritos = []
        for fav in favs:
            favoritos.append(Place.objects.all().get(pk=fav.lugar_id))
        if request.user.has_perm('auth.change_user') or item.pk == request.user.pk:
            grupo = str(item.groups.get())
            return render(request, 'user_info.html', {'item': item, 'item_list': item_list, 'grupo': grupo, 'form': form, 'profile': profile_form, 'favoritos': favoritos, 'mensaje': mensaje})
        else:
            return render(request, 'denied.html')

@login_required
@permission_required('auth.change_user', login_url='denied')
def user_list(request):
    item_list = User.objects.filter(is_superuser=False).order_by('username')
    return render(request, 'user_list.html', {'item_list': item_list})

# -------------------------------------------------------------------------------
# VISTAS para los lugares
# -------------------------------------------------------------------------------
@login_required
@permission_required('PFC.add_place', login_url='denied')
def new_place(request, tp):
    if tp == "site":
        tipo = "site"
    else:
        tipo = "poi"

    if request.method == "POST":
        form = PlaceForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            item = form.save(commit=False)
            item.votes = 1
            item.likes = 0
            item.author = request.user.pk
            item.save()
            request.session['nplaces'] = Place.objects.count()
            request.session['nsites'] = Place.objects.filter(tipo='site').count()
            request.session['npois'] = Place.objects.filter(tipo='poi').count()
            return redirect('place_info', pk=item.pk)
        else:
            return render(request, 'new_place.html', {'form': form, 'tipo': tipo})
    else:
        form = PlaceForm()
    return render(request, 'new_place.html', {'form': form, 'tipo': tipo})

@login_required
@permission_required('PFC.change_place', login_url='denied')
def edit_place(request, pk):
    item = get_object_or_404(Place, pk=pk)
    if item.author == request.user.pk:
        if request.method == "POST":
            form = PlaceForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                item = form.save(commit=False)
                item.save()
                return redirect('place_info', pk=item.pk)
        else:
            form = PlaceForm(instance=item)
        return render(request, 'edit_place.html', {'form': form})
    else:
        return redirect('denied')

@login_required
@permission_required('PFC.delete_place', login_url='denied')
def delete_place(request, pk, list):
    item = get_object_or_404(Place, pk=pk)
    tipo = item.tipo
    lista = list + "_list.html"
    print(lista)
    item.delete()
    request.session['nplaces'] = Place.objects.count()
    request.session['nsites'] = Place.objects.filter(tipo='site').count()
    request.session['npois'] = Place.objects.filter(tipo='poi').count()
    request.session['mensaje'] = 'Lugar eliminado con éxito'
    if list == 'profile':
        return redirect('user_info', pk=request.user.pk)
    # LO SIGUIENTE PUEDE SOBRAR
    elif list == 'place':
        item_list = Place.objects.all()
        tipo = 'place'
        return render(request, lista, {'item_list': item_list, 'tipo': tipo})
    else:
        if tipo == "site":
            item_list = Place.objects.filter(tipo='site')
            return render(request, lista, {'item_list': item_list, 'tipo': tipo})
        else:
            item_list = Place.objects.filter(tipo='poi')
            return render(request, lista, {'item_list': item_list, 'tipo': tipo})

@login_required
def place_info(request, pk):
    item = get_object_or_404(Place, pk=pk)
    item_list = Photo.objects.filter(place_id=pk)
    ref_list = Place.objects.filter(ref_id=pk)
    itemloc = (item.latitude, item.longitude)
    # if 'userlatlon' in request.session:
    #     loc = request.session['userlatlon']
    #     distancia = round(vincenty(loc, itemloc).km)
    # else:
    #     distancia = None
    distancia = None
    rating = int(item.rating)/10
    lugar = Place.objects.get(pk=pk)
    if Favoritos.objects.filter(lugar_id=lugar.pk).filter(usuario_id=request.user.pk):
        favorito = True
    else:
        favorito = False
    if Votos.objects.filter(lugar_id=lugar.pk).filter(usuario_id=request.user.pk):
        voto_usuario = Votos.objects.filter(lugar_id=lugar.pk).get(usuario_id=request.user.pk)
        voto_usuarionum = int(int(voto_usuario.valor)/10)
        voto = True
    else:
        voto = False
        voto_usuarionum = None
    return render(request, 'place_info.html', {'item': item, 'item_list': item_list, 'distancia': distancia, 'ref_list': ref_list, 'favorito': favorito, 'voto': voto, 'rating': rating, 'voto_usuarionum': voto_usuarionum})

@login_required
def place_list(request, tp):
    if tp == 'place':
        item_list = Place.objects.all().order_by('-rating')
    else:
        item_list = Place.objects.all().order_by('-rating').filter(tipo=tp)

    lista = item_list
    categoria = request.GET.get('cat')
    cat = []
    if categoria == None:
        if 'filtros' in request.session:
            #Borro la variable de sesion porque estoy renderizando la primera vez
            del request.session['filtros']
            return render(request, 'place_list.html', {'item_list': item_list, 'cats': cat, 'tipo': tp})
    else:
        if not 'filtros' in request.session:
            request.session['filtros'] = []
            #Creo variable de sesion filtros
            request.session['filtros'].append(categoria)
            #Incluyo la categoria que hemos seleccionado
        else:
            b = request.session['filtros']
            if categoria in b:
                #Ya está añadida
                b.remove(categoria)
                request.session['filtros'] = b
            else:
                #filtros no es nulo, así que intento incluir las nuevas categorias
                a = request.session['filtros']
                b.append(categoria)
                request.session['filtros'] = b
    switcher = {
        "Arte y diseño": 0,
        "Arquitectura": 1,
        "Historia": 2,
        "Ciencia y tecnología": 3,
        "Naturaleza": 4,
        "Aventura": 5,
        "Literatura": 6,
        "Música": 7,
        "Vida urbana": 8
    }

    if 'filtros' in request.session:
        filtros = request.session['filtros']
        cat = []
        n = 0
        for i in filtros:
            cat.append(switcher.get(i))
            item_list = lista.filter(categorias__contains=cat[n])
            lista = item_list
            n = n + 1
    return render(request, 'place_list.html', {'item_list': item_list, 'cats':cat, 'tipo': tp})

# -------------------------------------------------------------------------------
# VISTAS para el funcionamiento de la aplicación
# -------------------------------------------------------------------------------
def home(request):
    mensaje = ''
    if 'mensaje' in request.session:
        mensaje = request.session['mensaje']
        del request.session['mensaje']
    print(mensaje)
    request.session['nplaces'] = Place.objects.count()
    request.session['nsites'] = Place.objects.filter(tipo='site').count()
    request.session['npois'] = Place.objects.filter(tipo='poi').count()
    return render(request, 'home.html', {'mensaje': mensaje})

@login_required
def favoritos(request):
    if request.method == 'POST':
        print(request.POST)
        usuario_pk = request.POST.get('usuario')
        user = User.objects.all().get(pk=usuario_pk)
        lugar_pk = request.POST.get('lugar')
        place = Place.objects.all().get(pk=lugar_pk)
        formp = PlaceForm(instance=place)
        form = FavoritosForm(request.POST)
        print(form)
        if form.is_valid():
            if Favoritos.objects.all().filter(usuario_id=usuario_pk).filter(lugar_id=lugar_pk):
                print('Ya existe la pareja usuario y lugar en la tabla')
                Favoritos.objects.all().filter(usuario_id=usuario_pk).filter(lugar_id=lugar_pk).delete()
                itemp = formp.save(commit=False)
                likes = itemp.likes
                print(likes)
                itemp.likes = likes - 1
                print(place.likes)
                itemp.save()
            else:
                print('else guardo el item')
                item = form.save(commit=False)
                item.usuario_id = usuario_pk
                item.lugar_id = lugar_pk
                item.save()
                itemp = formp.save(commit=False)
                likes = itemp.likes
                print(likes)
                itemp.likes = likes + 1
                print(place.likes)
                itemp.save()
        else:
            print('Formulario no valido')
    return redirect('place_info', pk=lugar_pk)

@login_required
def votos(request):
    if request.method == 'POST':
        usuario_pk = request.POST.get('usuario')
        lugar_pk = request.POST.get('lugar')
        puntuacion = request.POST.get('valor')
        place = Place.objects.all().get(pk=lugar_pk)
        formp = PlaceForm(instance=place)
        form = VotosForm(request.POST)
        if form.is_valid():
            if Votos.objects.all().filter(usuario_id=usuario_pk).filter(lugar_id=lugar_pk):
                Votos.objects.all().filter(usuario_id=usuario_pk).filter(lugar_id=lugar_pk).delete()
                itemp = formp.save(commit=False)
                rating = itemp.rating
                votes = itemp.votes
                itemp.rating = (int(rating) * int(votes) - int(puntuacion) * 10) / (itemp.votes - 1)
                itemp.votes = votes - 1
                itemp.save()
            else:
                print('Se procede a puntuar')
                item = form.save(commit=False)
                item.usuario_id = usuario_pk
                item.lugar_id = lugar_pk
                item.valor = puntuacion
                item.save()
                itemp = formp.save(commit=False)
                rating = itemp.rating
                votes = itemp.votes
                itemp.rating = (int(rating) * int(votes) + int(puntuacion))/(itemp.votes + 1)
                itemp.votes = votes + 1
                itemp.save()
        else:
            print('Formulario no valido')
    return redirect('place_info', pk=lugar_pk)

@login_required
@permission_required('PFC.add_photo', login_url='denied')
def add_photo(request, pk):
    ref = pk
    item_list = Photo.objects.filter(place_id=pk)
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            return redirect('add_photo', pk=pk)
    else:
        form = PhotoForm()
    return render(request, 'add_photo.html', {'form': form, 'ref': ref, 'item_list': item_list})

@login_required
@permission_required('PFC.delete_photo', login_url='denied')
def del_photo(request, pk):
    item = Photo.objects.get(pk=pk)
    place_pk = item.place_id
    item.delete()
    return redirect('add_photo', pk=place_pk)

@login_required
def galery(request, pk):
    item_list = Photo.objects.filter(place_id=pk)
    return render(request, 'galeria.html', {'item_list': item_list})

# -------------------------------------------------------------------------------
# VISTAS para las recomendaciones
# -------------------------------------------------------------------------------
@login_required
def recomend(request):
    return render(request, 'recomend.html')

@login_required
def recomendaciones(request):
    nresultados = request.POST.get('nresultados')
    print(nresultados)

    # Recuperamos los parámetros de la búsqueda: C[ategorias], D[istancia], V(aloración], L[ocalizacion], y P[rioridad]
    C = []
    for c in range(0,10,1):
        if request.POST.get('categoria'+str(c)):
            C.append(int(request.POST.get('categoria'+str(c))))
    # Si el usuario no ha seleccionado ninguna categoría, incluimos todas en la búsqueda
    if C == []:
        C = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    D = request.POST.get('distancia')
    V = request.POST.get('valoracion')
    L = request.POST.get('localizacion')
    P = request.POST.get('prioridad')

    # Asignamos los pesos a los distintos criterios en tanto por 1
    porcentaje_cat = int(P[0])/10
    porcentaje_dis = int(P[1])/10
    porcentaje_val = int(P[2])/10

    # Elemento para tratar las categorías más adelante
    switcher = {
        0: "Arte y diseño",
        1: "Arquitectura",
        2: "Historia",
        3: "Ciencia y tecnología",
        4: "Naturaleza",
        5: "Aventura",
        6: "Literatura",
        7: "Música",
        8: "Vida urbana"
    }

    # Arrays
    cat_seleccionadas = C
    distancia_elegida = int(D)
    valoracion_elegida = int(V)
    lugares_coincidentes = []
    lugares_distintos = []
    distancias = []
    distancias_inv = []
    puntuacion = 0
    puntuaciones_totales = []
    puntuaciones_finales = []
    resultado = []
    valoraciones = []

    # Tratamos de averiguar las coordenadas del lugar que el usuario ha introducido como origen de la búsqueda
    if L:
        while True:
            try:
                geolocator = Nominatim()
                localizacion = geolocator.geocode(L)
                posicion = (localizacion.latitude, localizacion.longitude)
                break
            # Si hay error en la detección, volvemos al formulario y le decimos que introduzca una dirección válida
            except AttributeError:
                error = "Dirección no válida. Por favor inténtelo de nuevo"
                return render(request, 'recomend.html', {'error': error})
    # Si el usuario no ha introducido ningún lugar intentamos saber su ubicación
    else:
        if 'userlatlon' in request.session:
            localizacion = 'Tu ubicación'
            posicion = request.session['userlatlon']
        # Si no se introdujo ninguna dirección y no se pudo localizar al usuario mediante su IP (por ejemplo porque no tenga conexión a internet) volvemos al formulario para que introduzca una dirección
        else:
            error = 'No fue posible usar tu ubicación. Por favor introduce una dirección válida'
            return render(request, 'recomend.html', {'error': error})

    # Seleccionamos los lugares que tienen al menos una categoría de las seleccionadas
    for categoria in cat_seleccionadas:
        lugares = Place.objects.all().filter(categorias__contains=categoria)
        for lugar in lugares:
            lugares_coincidentes.append(lugar)

    # Y restringimos la lista a aquellos lugares que son distrintos entre sí
    for lugar in lugares_coincidentes:
        if lugar not in lugares_distintos:
            lugares_distintos.append(lugar)



    # Para cada lugar diferente, rellenamos el array de resultados con sus datos.
    # Datos = lugar, nºcategorias coincidentes, distancia, valoración de los usuarios (sobre 100 y sobre 10), y la puntuación de la recomendación
    # La Puntuación sólo se inicializa
    for lugar in lugares_distintos:
        veces = lugares_coincidentes.count(lugar)
        posicion_lugar = (lugar.latitude, lugar.longitude)
        distancia = round(vincenty(posicion_lugar, posicion).km)
        valoracion = lugar.rating
        nota_usuarios = int(valoracion) / 10
        cat_coincidentes = []
        cat_lugar = []

        for c in lugar.categorias:
            cat_lugar.append(int(c))
        for c in cat_seleccionadas:
            if c in cat_lugar:
                cat_coincidentes.append(switcher.get(c))
        if distancia < distancia_elegida and valoracion > valoracion_elegida:
            distancias.append(distancia)
            valoraciones.append(valoracion)
            resultado.append([lugar, veces, distancia, [valoracion, nota_usuarios], cat_coincidentes, puntuacion])
    print(valoraciones)
    if valoraciones != []:
        valoracion_max = max(valoraciones)
        valoracion_min = min(valoraciones)

    # Cálculo de la distancia inversa de cara a calcular la puntuación por distancia
    for item in resultado:
        distancias_inv.append((item[2] - max(distancias)) * (-1))
    # Calculo de las puntuaciones por criterios
    for item in resultado:
        ptos_cat = item[1]*100/int(len(cat_seleccionadas))

        ptos_val = (100*(item[0].rating - valoracion_min))/(valoracion_max - valoracion_min)

        # ptos_val = item[0].rating
        if max(distancias) == min(distancias):
            ptos_dis = 100
        else:
            ptos_dis = ((item[2] - max(distancias)) * (-1))*100/max(distancias_inv)
        ptos_totales = round((ptos_cat*porcentaje_cat)+(ptos_val*porcentaje_val)+(ptos_dis*porcentaje_dis))
        item[5] = ptos_totales
        puntuaciones_totales.append(ptos_totales)
        print(str(item[0]) + ': CAT(' + str(round(ptos_cat)) + ')|VAL(' + str(round(ptos_val)) + ')|DIS(' + str(round(ptos_dis)) + ')|TOTAL(' + str(round(ptos_totales)) + ')')
    # Normalización de las puntuaciones sobre 100%
    for puntuacion in puntuaciones_totales:
        puntuaciones_finales.append(round(puntuacion/max(puntuaciones_totales)*100))

    # Incluimos las puntuaciones finales calculadas en el array de resultado y lo ordenamos por este valor
    for item in resultado:
        item[5] = puntuaciones_finales[resultado.index(item)]
    resultado.sort(key=lambda x: x[5], reverse=True)


    # Si el usuario seleccionó mostrar solo el top 10 de resultados, alteramos el array de resultados para que sólo tenga 10 elementos
    if nresultados:
        diezresultados = []
        if len(resultado) < int(nresultados):
            nresultados = len(resultado)
        for n in range(int(nresultados)):
            diezresultados.append(resultado[n])
        resultado = diezresultados
    # arámetros se usa en la página html
    parametros = [localizacion, posicion]

    if not resultado:
        print('No hay ningun lugar asociado a la búsqueda')
        return redirect('nolugares')

    # Finalmente devolvemos el resultado del algoritmo de recomendaciones
    return render(request, 'recomendaciones.html', {'resultado': resultado, 'parametros':parametros})

# -------------------------------------------------------------------------------
# VISTAS para la web API
# -------------------------------------------------------------------------------
@csrf_exempt
def getSites(request):
    t = request.POST.get('time')
    print(t)
    if t:
        suma = 3+5
        print(suma)
    else:
        print('no se ha pasado time')
    sites = Place.objects.all().filter(tipo='site')
    n = len(sites)
    datos_mini = {}
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for i in range(n):
        path = os.path.join(BASE_DIR, '/media/', str(sites[i].image).lstrip('./'))
        datos_mini[i] = [sites[i].id, sites[i].name, sites[i].latitude, sites[i].longitude, path]
    return JsonResponse(datos_mini, content_type='application/json')

@csrf_exempt
def getPlaceDetails(request):
    placeid = request.POST.get('placeid')

    site = Place.objects.get(pk=placeid)
    pois = Place.objects.all().filter(ref_id=placeid)
    n = len(pois)
    datos_extra = {}
    datos_mini = {}
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    siteimgpath = os.path.join(BASE_DIR, '/media/', str(site.image).lstrip('./'))
    for i in range(n):
        path = os.path.join('/media/', str(pois[i].image).lstrip('./'))
        datos_mini[i] = [pois[i].id, pois[i].name, pois[i].latitude, pois[i].longitude, path]
    datos_extra[0] = site.id
    datos_extra[1] = site.name
    datos_extra[2] = site.latitude
    datos_extra[3] = site.longitude
    datos_extra[4] = siteimgpath
    datos_extra[5] = site.description
    datos_extra[6] = site.categorias
    datos_extra[7] = site.url
    datos_extra[8] = site.rating
    datos_extra[9] = site.votes
    datos_extra[10] = site.likes
    datos_extra[11] = datos_mini
    return JsonResponse(datos_extra, content_type='application/json')

@csrf_exempt
def setFavorite(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    placeid = request.POST.get('placeid')

    resultado = {}
    resultado[0] = "ERROR"
    resultado[1] = "USERNAME O PASSWORD INCORRECTOS"
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        resultado[1] = 'EL LUGAR QUE INTENTA MARCAR COMO FAVORITO NO EXISTE'
        if Place.objects.all().filter(pk=placeid):
            place = Place.objects.all().get(pk=placeid)
            formp = PlaceForm(instance=place)
            form = FavoritosForm()
            if Favoritos.objects.all().filter(usuario_id=user.pk).filter(lugar_id=placeid):
                Favoritos.objects.all().filter(usuario_id=user.pk).filter(lugar_id=placeid).delete()
                itemp = formp.save(commit=False)
                likes = itemp.likes
                itemp.likes = likes - 1
                itemp.save()
                resultado[0] = 'OK'
                resultado[1] = 'UNLIKE'
            else:
                item = form.save(commit=False)
                item.usuario_id = user.pk
                item.lugar_id = placeid
                item.save()
                itemp = formp.save(commit=False)
                likes = itemp.likes
                itemp.likes = likes + 1
                itemp.save()
                resultado[0] = 'OK'
                resultado[1] = 'LIKE'
    return JsonResponse(resultado, content_type='application/json')

@csrf_exempt
def setFeedback(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    placeid = request.POST.get('placeid')
    score = request.POST.get('score')

    resultado = {}
    resultado[0] = "ERROR"
    resultado[1] = 'PUNTUACIÓN FUERA DE LOS LÍMITES'
    if score >= 0 and score <= 100:
        resultado[1] = "USERNAME O PASSWORD INCORRECTOS"
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            resultado[1] = 'EL LUGAR AL QUE INTENTA VOTAR NO EXISTE'
            if Place.objects.all().filter(pk=placeid):
                place = Place.objects.all().get(pk=placeid)
                formp = PlaceForm(instance=place)
                form = VotosForm()
                if Votos.objects.all().filter(usuario_id=user.pk).filter(lugar_id=placeid):
                    Votos.objects.all().filter(usuario_id=user.pk).filter(lugar_id=placeid).delete()
                    itemp = formp.save(commit=False)
                    rating = itemp.rating
                    votes = itemp.votes
                    itemp.rating = (int(rating) * int(votes) - int(score)) / (itemp.votes - 1)
                    itemp.votes = votes - 1
                    itemp.save()
                    resultado[0] = 'OK'
                    resultado[1] = 'VOTO DEL USUARIO RESETEADO'
                else:
                    item = form.save(commit=False)
                    item.usuario_id = user.pk
                    item.lugar_id = placeid
                    item.valor = score
                    item.save()
                    itemp = formp.save(commit=False)
                    rating = itemp.rating
                    votes = itemp.votes
                    itemp.rating = (int(rating) * int(votes) + int(score)) / (itemp.votes + 1)
                    itemp.votes = votes + 1
                    itemp.save()
                    resultado[0] = 'OK'
                    resultado[1] = 'VOTO DEL USUARIO ANOTADO'
    return JsonResponse(resultado, content_type='application/json')

@csrf_exempt
def getRecommendations(request):
    resultado = {}
    resultado[0] = "ERROR"
    resultado[1] = "El usuario no existe o los datos son erróneos"
    username = request.POST.get('username')
    password = request.POST.get('password')
    criterio = int(request.POST.get('criterion'))
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        if criterio == 1:
            sitios = []
            sites = Place.objects.all().order_by('categorias')
            print('El criterio elegido es Categorías')
            for site in sites:
                sitios.append([site, len(site.categorias)])
            sitios.sort(key=lambda x: x[1], reverse=True)
            datos_mini = {}
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            for i in range(25):
                path = os.path.join(BASE_DIR, '/media/', str(sites[i].image).lstrip('./'))
                print(sitios[i][0])
                datos_mini[i] = [sitios[i][0].id , sitios[i][0].name, sitios[i][0].latitude, sitios[i][0].longitude, path]
            return JsonResponse(datos_mini, content_type='application/json')
        elif criterio == 2:
            sites = Place.objects.all().order_by('-likes')
            print('El criterio elegido es Popularidad')
            n = len(sites)
            datos_mini = {}
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            for i in range(n):
                path = os.path.join(BASE_DIR, '/media/', str(sites[i].image).lstrip('./'))
                datos_mini[i] = [sites[i].id, sites[i].name, sites[i].latitude, sites[i].longitude, path]
            return JsonResponse(datos_mini, content_type='application/json')
        elif criterio == 3:
            sites = Place.objects.all().order_by('-rating')
            print('El criterio elegido es Ranking')
            n = len(sites)
            datos_mini = {}
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            for i in range(n):
                path = os.path.join(BASE_DIR, '/media/', str(sites[i].image).lstrip('./'))
                datos_mini[i] = [sites[i].id, sites[i].name, sites[i].latitude, sites[i].longitude, path]
            return JsonResponse(datos_mini, content_type='application/json')
        else:
            resultado[1] = "El criterio está fuera de rango"
    return JsonResponse(resultado, content_type='application/json')

@csrf_exempt
def createUser(request):
    resultado={}
    resultado[0]='ERROR'
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = User.objects.create_user(username=username, password=password)
        user.save
        profile_form = ProfileForm()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.tipo = 'usuarios'
        profile.save()
        user.groups.add(Group.objects.get(name='usuarios'))
        resultado[0]='USUARIO CREADO'
        return JsonResponse(resultado, content_type='application/json')
    except IntegrityError:
        resultado[0]='EL USUARIO YA EXISTE'
        return JsonResponse(resultado, content_type='application/json')

@csrf_exempt
def deleteUser(request):
    resultado={}
    resultado[0] = 'El Usuario NO existe'
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        user.delete()
        resultado[0] = 'Usuario eliminado con éxito'
        return JsonResponse(resultado, content_type='application/json')
    else:
        return JsonResponse(resultado, content_type='application/json')
