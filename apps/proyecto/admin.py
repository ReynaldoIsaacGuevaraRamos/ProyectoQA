from django.contrib import admin

from .models import *

admin.site.register(Agencia)
admin.site.register(Departamento)
admin.site.register(Comite)
admin.site.register(Actividad)
admin.site.register(EncuestaCliente)
admin.site.register(RespuestaEncuestaCliente)
admin.site.register(EncuestaPersonal)
admin.site.register(RespuestaEncuestaPersonal)
admin.site.register(Empleado)