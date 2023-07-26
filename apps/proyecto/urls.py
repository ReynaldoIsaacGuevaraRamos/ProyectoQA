from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static 
 
app_name = 'evaluacionCliente'

urlpatterns = [
    
    # URL de base 
    path('',index),
    path('evaluacionCliente/index/',index, name='index'),

    # URL envio de correo
    path('evaluacionCliente/send_email/<str:agencia>/<str:departamento>/<str:comite>/', login_required(enviarEmail), name='send_email'),
    path('evaluacionCliente/listar_empleado_correo/', login_required(listarEmpleadosCorreo), name='listar_empleado_correo'),        
    path('evaluacionCliente/filtrarEmpleadosCorreo/', login_required(filtrarEmpleadosCorreo), name="filtrar_empleados_correo"),
    path('evaluacionCliente/enviar_correo/<str:agencia>/<str:departamento>/<str:comite>/', login_required(enviarCorreo), name="enviar_correo"),
    path('evaluacionCliente/confirmar_invitacion/', login_required(confirmarInvitacion), name="confirmar_invitacion"),

	#URLs para Departamento
    path('evaluacionCliente/crear_departamento/', login_required(crearDepartamento), name='crear_departamento'),
    path('evaluacionCliente/listar_departamento/', login_required(listarDepartamento), name='listar_departamento'),
    path('evaluacionCliente/editar_departamento/<codigo_departamento>/', login_required(editarDepartamento), name='editar_departamento'),
    path('evaluacionCliente/eliminar_departamento/<pk>/', login_required(eliminarDepartamento.as_view()), name='eliminar_departamento'),

	#URLs para Comites
    path('evaluacionCliente/crear_comite/', login_required(crearComite), name='crear_comite'),
    path('evaluacionCliente/listar_comite/', login_required(listarComite), name='listar_comite'),
    path('evaluacionCliente/editar_comite/<id_comite>/', login_required(editarComite), name='editar_comite'),
    path('evaluacionCliente/eliminar_comite/<pk>/', login_required(eliminarComite.as_view()), name='eliminar_comite'),

	#URLs para Agenciaa
    path('evaluacionCliente/crear_agencia/', login_required(crearAgencia), name='crear_agencia'),
    path('evaluacionCliente/listar_agencia/', login_required(listarAgencia), name='listar_agencia'),    
    path('evaluacionCliente/editar_agencia/<codigo_agencia>/', login_required(editarAgencia), name='editar_agencia'),
    path('evaluacionCliente/eliminar_agencia/<pk>/', login_required(eliminarAgencia.as_view()), name='eliminar_agencia'),

    #URLs para Actividades
    path('evaluacionCliente/crear_actividad/', login_required(crearActividad), name='crear_actividad'),
    path('evaluacionCliente/listar_actividad/', login_required(listarActividad), name='listar_actividad'),    
    path('evaluacionCliente/editar_actividad/<id_actividad>/', login_required(editarActividad), name='editar_actividad'),
    path('evaluacionCliente/eliminar_actividad/<pk>/', login_required(eliminarActividad.as_view()), name='eliminar_actividad'),

    #URLs para Empleados
    path('evaluacionCliente/crear_empleado/', login_required(crearEmpleado), name='crear_empleado'),
    path('evaluacionCliente/listar_empleados/', login_required(listarEmpleados), name='listar_empleados'),    
    path('evaluacionCliente/editar_empleado/<id_empleado>/', login_required(editarEmpleado), name='editar_empleado'),
    path('evaluacionCliente/eliminar_empleado/<pk>/', login_required(eliminarEmpleado.as_view()), name='eliminar_empleado'),
    path('evaluacionCliente/filtrarEmpleados/', login_required(filtrarEmpleados), name="filtrar_empleados"),
    path('evaluacionCliente/reporteEmpleadosPDF/<str:agencia>/<str:departamento>/<str:comite>/', login_required(reporteEmpleadosPDF), name="reporte_empleadosPDF"),
    path('evaluacionCliente/exportarEmpleadosCSV/<str:agencia>/<str:departamento>/<str:comite>/', login_required(exportarEmpleados), name="reporte_empleadosCSV"),

    #URLs para Encuesta Cliente
    path('evaluacionCliente/listar_encuesta/', login_required(listarEncuesta), name='listar_encuesta'),
    path('evaluacionCliente/listar_encuesta/Agencia/', login_required(consultarAgencia), name='consultar_agencia'),
    path('evaluacionCliente/listar_encuesta/Agencia2/<str:codigoAgencia>/', login_required(consultarAgencia2), name='consultar_agencia2'),
    path('evaluacionCliente/listar_encuesta/Encuesta/<str:codigoAgencia>', login_required(consultarEncuesta), name='consultar_encuesta'),
    path('evaluacionCliente/listar_encuesta/Encuesta2/<str:codigoAgencia>/<str:tituloEncuesta>/', login_required(consultarEncuesta2), name='consultar_encuesta2'),
    path('evaluacionCliente/listar_encuesta/Preguntas/<str:codigoAgencia>/<str:tituloEncuesta>/', login_required(AgregarPreguntasEncuestaCliente), name='agregar_preguntas_encuesta_cliente'),

    path('evaluacionCliente/crear_encuesta/<str:codigoAgencia>/', login_required(crearEncuesta), name='crear_encuesta'),
    path('evaluacionCliente/editar_encuesta/<int:idEncuesta>/', login_required(editarEncuesta), name='editar_encuesta'),
    path('evaluacionCliente/eliminar_encuesta/<int:idEncuesta>/', login_required(eliminarEncuesta), name='eliminar_encuesta'),

    path('evaluacionCliente/editar_informacion_encuesta/<int:idEncuesta>/', login_required(editarInfEncuesta), name='editar_inf_encuesta'),

    path('evaluacionCliente/contestar_encuesta/', contestarEncuesta, name='contestar_encuesta'),
    path('evaluacionCliente/encuesta/Agencia/', consultarAgenciaEncuesta, name='consultar_agencia_encuesta'),
    path('evaluacionCliente/encuesta/Encuesta/<str:codigoAgencia>', consultarEncuestaCliente, name='consultar_encuesta_cliente'),
    path('evaluacionCliente/encuesta/Encuesta2/<str:codigoAgencia>', consultarEncuestaCliente2, name='consultar_encuesta2'),
    path('evaluacionCliente/encuesta/Encuesta22/<str:codigoAgencia>/<str:tituloEncuesta>', consultarEncuestaCliente22, name='consultar_encuesta22'),
    path('evaluacionCliente/encuesta/Respuesta/<str:codigoAgencia>/<str:tituloEncuesta>/<str:descripcionPregunta>/<int:contador>/', contestarEncuestaCliente, name='contestar_encuesta_cliente'),

    path('evaluacionCliente/Resultados/listar_agencia/', login_required(listarRespuestasEncuesta), name='listar_respuestas_encuesta'),
    path('evaluacionCliente/Resultados/listar_encuesta/', login_required(consultarRespuestasAgenciaCliente), name='consultar_agencia_respuestas_cliente'),
    path('evaluacionCliente/Resultados/listar_resultados/<str:codigoAgencia>', login_required(consultarRespuestasEncuestaCliente), name='consultar_respuestas_encuesta_cliente'),


    #URLs para Encuesta Personal
    path('evaluacionCliente/listar_encuesta_personal/', login_required(listarEncuestaPersonal), name='listar_encuesta_personal'),
    path('evaluacionCliente/listar_encuesta_personal/Actividad/', login_required(consultarActividadPersonal), name='consultar_actividad_personal'),
    path('evaluacionCliente/listar_encuesta_personal/Actividad2/<str:idActividad>/', login_required(consultarActividad2Personal), name='consultar_actividad2_personal'),
    path('evaluacionCliente/listar_encuesta_personal/Encuesta/<str:idActividad>', login_required(consultarEncuestaPersonal), name='consultar_encuesta_personal'),
    path('evaluacionCliente/listar_encuesta_personal/Encuesta2/<str:idActividad>/<str:tituloEncuesta>/', login_required(consultarEncuesta2Personal), name='consultar_encuesta2_personal'),
    path('evaluacionCliente/listar_encuesta_personal/Preguntas/<str:idActividad>/<str:tituloEncuesta>/', login_required(AgregarPreguntasEncuestaPersonal), name='agregar_preguntas_encuesta_personal'),

    path('evaluacionCliente/crear_encuesta_personal/<str:idActividad>/', login_required(crearEncuestaPersonal), name='crear_encuesta_personal'),
    path('evaluacionCliente/editar_encuesta_personal/<int:idEncuesta>/', login_required(editarEncuestaPersonal), name='editar_encuesta_personal'),
    path('evaluacionCliente/eliminar_encuesta_personal/<int:idEncuesta>/', login_required(eliminarEncuestaPersonal), name='eliminar_encuesta_personal'),
    
    path('evaluacionCliente/editar_informacion_encuesta_personal/<int:idEncuesta>/', login_required(editarInfEncuestaPersonal), name='editar_inf_encuesta_personal'),

    path('evaluacionCliente/contestar_encuesta_personal/', contestarEncuestaPersonal, name='contestar_encuesta_personal'),
    path('evaluacionCliente/encuestaPersonal/Actividad/', consultarActividadEncuestaDePersonal, name='consultar_actividad_encuesta_de_personal'),
    path('evaluacionCliente/encuestaPersonal/Encuesta/<str:idActividad>', consultarEncuestaDePersonal, name='consultar_encuesta_de_personal'),
    path('evaluacionCliente/encuestaPersonal/Encuesta2/<str:idActividad>', consultarEncuestaDePersonal2, name='consultar_encuesta_de_personal2'),
    path('evaluacionCliente/encuestaPersonal/Encuesta22/<str:idActividad>/<str:tituloEncuestaPersonal>', consultarEncuestaDePersonal22, name='consultar_encuesta_de_personal22'),
    path('evaluacionCliente/encuestaPersonal/Respuesta/<str:idActividad>/<str:tituloEncuesta>/<str:descripcionPregunta>/<int:contador>/', contestarEncuestaDePersonal, name='contestar_encuesta_de_personal'),

    path('evaluacionCliente/Resultados/listar_actividad/', login_required(listarRespuestasEncuestaPersonal), name='listar_respuestas_encuesta_personal'),
    path('evaluacionCliente/Resultados/listar_encuesta_personal/', login_required(consultarRespuestasActividadPersonal), name='consultar_actividad_respuestas_personal'),
    path('evaluacionCliente/Resultados/listar_resultados_encuesta/<str:idActividad>', login_required(consultarRespuestasEncuestaPersonal), name='consultar_respuestas_encuesta_personal'),

    #URLs para Reportes de Respuesta
    path('evaluacionCliente/Resultados/respuestas_encuestas_cliente/', login_required(reporteRespuestasEncuestaCliente), name='respuestas_encuestas_cliente'),
    path('evaluacionCliente/Resultados/respuestas_encuestas_personal/', login_required(reporteRespuestasEncuestaPersonal), name='respuestas_encuestas_personal'),

    #URLs para Exportar Respuestas a CSV
    path('evaluacionCliente/exportarResultadosEncuestaPersonal/', login_required(exportarRespuestasEncuestaPersonal), name="exportar_respuestas_encuesta_personal"),
    path('evaluacionCliente/exportarResultadosEncuestaCliente/', login_required(exportarRespuestasEncuestaCliente), name="exportar_respuestas_encuesta_cliente"),

]