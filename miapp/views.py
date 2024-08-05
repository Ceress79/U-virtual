from django.shortcuts import render, redirect
from .models import User, asignatura, horario, actividad
from .forms import updateUserForm, loginForm, calificacionForm, asignaturaForm, horarioForm, actividadForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView


# Inicio de sesión
class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = loginForm

# Cerrar sesión
class CustomLogoutView(LogoutView):
    next_page = 'login'

@login_required
# Vista de inicio
def index_view(request):
    links = [
        {'title': 'Asignatura', 'image': './img/cards/asignatura.png', 'url': 'asignatura'},
        {'title': 'Actividad', 'image': './img/cards/actividad.jpg', 'url': 'actividad'},
        {'title': 'Calificaciones', 'image': './img/cards/calificacion.jpg', 'url': 'calificacion'},
        {'title': 'Horario', 'image': './img/cards/horario.png', 'url': 'horario'},
        {'title': 'Citación', 'image': './img/cards/citacion.jpeg', 'url': '#'},
        {'title': 'Tutoria', 'image': './img/cards/tutoria.jpg', 'url': '#'},
        {'title': 'Conducta', 'image': './img/cards/conducta.jpg', 'url': '#'},
        {'title': 'Usuario', 'image': './img/cards/usuario.png', 'url': 'updateUser'},
    ]
    return render(request, 'miapp/home.html', {'links': links})

@login_required
# Vista de actualización de usuario
def updateUser_view(request):
    if request.method == 'POST':
        userForm = updateUserForm(request.POST, request.FILES)
        if userForm.is_valid():
            user = userForm.save(commit=False)
            password = request.POST.get('password')
            if password:  # Verificar si se proporcionó una contraseña
                user.set_password(password)  # Hashear la contraseña antes de guardarla
            userForm.save()
            return redirect('home')
    else:
        userForm = updateUserForm()  # Inicializa el formulario si la solicitud no es POST

    return render(request, 'Registration/registrar_usuario.html', {
        'formUser': userForm
    })

@login_required
def calificacion_view(request):
    usuario = None
    userSearch = False

    if request.method == 'GET' and 'dni' in request.GET:
        dni = request.GET.get('dni')
        if dni:
            try:
                usuario = User.objects.get(dni=dni)
                if usuario.rol == 'estudiante':
                    userSearch = True
                else:
                    usuario = None
                    userSearch = True
            except User.DoesNotExist:
                usuario = None
                userSearch = True  # Indicar que la búsqueda se realizó pero no se encontró el usuario

    if request.method == 'POST':
        Caliform = calificacionForm(request.POST)
        dni = request.POST.get('dni')
        if dni:
            try:
                usuario = User.objects.get(dni=dni)
            except User.DoesNotExist:
                usuario = None

        if Caliform.is_valid() and usuario:
            calificacion_instance = Caliform.save(commit=False)
            calificacion_instance.usuario = usuario
            calificacion_instance.save()
            return redirect('home')
    else:
        Caliform = calificacionForm()
    
    return render(request, 'miapp/registrar_calificacion.html', {
        'formCali': Caliform,
        'usuario': usuario,
        'userSearch': userSearch
    })




@login_required
def asignatura_view(request):
    if request.method == 'POST':
        asigForm = asignaturaForm(request.POST)
        if asigForm.is_valid():
            asigForm.save()
            return redirect('home')  
    else:
        asigForm = asignaturaForm()
    return render(request, 'miapp/registrar_asignatura.html', {
        'formAsig': asigForm
    })

@login_required
def actividad_view(request):
    if request.method == 'POST':
        activForm = actividadForm(request.POST)
        if activForm.is_valid():
            activForm.save()
            return redirect('home')
    else:
        activForm = actividadForm()
    return render(request, 'miapp/registrar_actividad.html', {
        'formActividad': activForm
    
    })


@login_required
def horario_view(request):
    if request.method == 'POST':
        horariForm = horarioForm(request.POST)
        if horariForm.is_valid():
            horariForm.save()
            return redirect('home')
    else:
        horariForm = horarioForm()
    return render(request, 'miapp/registrar_horario.html', {
        'formHorari': horariForm
        })