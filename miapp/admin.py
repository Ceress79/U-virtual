from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, asignatura, calificacion, horario, actividad

class adminUser(UserAdmin):
    list_display = ('dni', 'email', 'first_name', 'last_name', 'rol', 'is_staff')
    search_fields = ('dni', 'first_name', 'last_name', 'email')
    list_filter = ('rol', 'is_staff', 'is_active')
    list_per_page = 15

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'password1', 'password2', 'dni', 'email', 'rol', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    
admin.site.register(User, adminUser)


class adminAsignatura(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'curso', 'creditos')
    list_per_page = 15

admin.site.register(asignatura, adminAsignatura)


class adminCalificacion(admin.ModelAdmin):
    list_display = ('usuario', 'asignatura', 'actividad', 'nota', 'fecha_entrega', 'comentario')
    search_fields = ('usuario__first_name', 'usuario__last_name', 'asignatura__nombre', 'actividad')
    list_filter = ('usuario', 'asignatura', 'actividad')
    list_per_page = 15

admin.site.register(calificacion, adminCalificacion)

class adminActividad(admin.ModelAdmin):
    list_display = ('asignatura', 'nombre', 'descripcion', 'fecha_inicio', 
                    'fecha_fin','estado','comentario')
    list_per_page = 15

admin.site.register(actividad, adminActividad)


class adminHorario(admin.ModelAdmin):
    list_display = ('asignatura', 'dia', 'hora_inicio', 'hora_fin')
    list_filter = ('asignatura', 'dia')
    list_per_page = 15

admin.site.register(horario, adminHorario)