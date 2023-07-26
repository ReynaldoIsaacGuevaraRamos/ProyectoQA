from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.core import serializers
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from datetime import datetime

import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from SistemaACOPUS import settings
from django.template.loader import render_to_string

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from .models import *
import xlwt
import os

from .models import *
from .forms import *

#----------------------------------------------------------------------------------------------------------------------------------


#Vista para el menu base
def index(request):
    return render(
        request,
        'base/base.html'
    )


"""
Función para mostrar imagenes dentro de los reportes en PDF elaborados.
@param      una url relativa
@return     Retorna la configuración de Settings donde estan alojadas las imagenes
@author     Noel Renderos
"""

def link_callback(uri, rel):
    """
    Convierte HTML a URIs absoluta en el Path del sistema para que  xhtml2pdf
    tenga acceso a los recuros
    """
    result = finders.find(uri)

    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
    
        result = list(os.path.realpath(path) for path in result)
        path = result[0]
    
    else:
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL  # Typically /media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
    
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
    
        else:
            return uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    
    return path


#----------------------------------------------------------------------------------------------------------------------------------


#	CRUD DEPARTAMENTO

# Crear departamento
def crearDepartamento(request):
	if request.method == 'POST':
		departamento_form = DepartamentoForm(request.POST)
		if departamento_form.is_valid():
			departamento_form.save()
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_departamento'))  
	else:
		departamento_form = DepartamentoForm()
	return render(request, 'evaluacionCliente/crear_departamento.html', {'departamento_form': departamento_form})


# Vista para el Departamento
def listarDepartamento(request):
	departamentos = Departamento.objects.order_by('nombre_departamento')
	#Mandar la consulta al template
	return render(request, 'evaluacionCliente/listar_departamento.html', {'departamentos': departamentos})		


# Editar Departamento
def editarDepartamento(request, codigo_departamento):
	departamento_form = None
	error = None

	try:
		departamento =Departamento.objects.get(codigo_departamento = codigo_departamento)
		if request.method =='GET':
			departamento_form=DepartamentoForm(instance = departamento)
		else:
			departamento_form = DepartamentoForm(request.POST, instance = departamento)
			if departamento_form.is_valid():
				departamento_form.save()
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_departamento'))
	except ObjectDoesNotExist as e:
		error = e
	return render(request, 'evaluacionCliente/editar_departamento.html', {'departamento_form': departamento_form, 'error':error})


# Eliminar Departamento
class eliminarDepartamento(DeleteView):
    model = Departamento
    template_name = 'evaluacionCliente/listar_departamento.html'
    success_url = reverse_lazy('evaluacionCliente:listar_departamento')


#----------------------------------------------------------------------------------------------------------------------------------


#	CRUD COMITE

# Crear Comite
def crearComite(request):
	if request.method == 'POST':
		comite_form = ComiteForm(request.POST)
		if comite_form.is_valid():
			comite_form.save()
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_comite'))  
	else:
		comite_form = ComiteForm()
	return render(request, 'evaluacionCliente/crear_comite.html', {'comite_form': comite_form})


# Vista para el Comite
def listarComite(request):
	comites = Comite.objects.order_by('nombre_comite')
	#Mandar la consulta al template
	return render(request, 'evaluacionCliente/listar_comite.html', {'comites': comites})	


# Editar Comite
def editarComite(request, id_comite):
	comite_form = None
	error = None

	try:
		comite = Comite.objects.get(id_comite = id_comite)
		if request.method =='GET':
			comite_form=ComiteForm(instance = comite)
		else:
			comite_form = ComiteForm(request.POST, instance = comite)
			if comite_form.is_valid():
				comite_form.save()
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_comite'))
	except ObjectDoesNotExist as e:
		error = e
	return render(request, 'evaluacionCliente/editar_comite.html', {'comite_form': comite_form, 'error':error})


# Eliminar Comite
class eliminarComite(DeleteView):
    model = Comite
    template_name = 'evaluacionCliente/listar_comite.html'
    success_url = reverse_lazy('evaluacionCliente:listar_comite')


#----------------------------------------------------------------------------------------------------------------------------------


#	CRUD AGENCIA

# Crear Agencia
def crearAgencia(request):
	if request.method == 'POST':
		agencia_form =AgenciaForm(request.POST)
		if agencia_form.is_valid():
			agencia_form.save()
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_agencia'))  
	else:
		agencia_form = AgenciaForm()
	return render(request, 'evaluacionCliente/crear_agencia.html', {'agencia_form': agencia_form})


# Vista para la Agencia
def listarAgencia(request):
	agencias = Agencia.objects.order_by('nombre_agencia')
	#Mandar la consulta al template
	return render(request, 'evaluacionCliente/listar_agencia.html', {'agencias': agencias})


# Editar Agencia
def editarAgencia(request, codigo_agencia):
	agencia_form = None
	error = None

	try:
		agencia = Agencia.objects.get(codigo_agencia = codigo_agencia)
		if request.method =='GET':
			agencia_form=AgenciaForm(instance = agencia)
		else:
			agencia_form = AgenciaForm(request.POST, instance = agencia)
			if agencia_form.is_valid():
				agencia_form.save()
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_agencia'))
	except ObjectDoesNotExist as e:
		error = e
	return render(request, 'evaluacionCliente/editar_agencia.html', {'agencia_form': agencia_form, 'error':error})


# Eliminar Agencia
class eliminarAgencia(DeleteView):
    model = Agencia
    template_name = 'evaluacionCliente/listar_agencia.html'
    success_url = reverse_lazy('evaluacionCliente:listar_agencia')


#----------------------------------------------------------------------------------------------------------------------------------


#	CRUD ACTIVIDADES

# Crear Actividad
def crearActividad(request):
	if request.method == 'POST':
		actividad_form = ActividadForm(request.POST)
		if actividad_form.is_valid():
			actividad_form.save()
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_actividad'))  
	else:
		actividad_form = ActividadForm()
		# contexto {
		# 	agencias = Agencia.objects.order_by('codigo_agencia')
		# 	departamentos = Departamento.objects.order_by('codigo_departamento')
		# 	comites = Comite.objects.order_by('nombre_comite')
		# }

	return render(request, 'evaluacionCliente/crear_actividad.html', {'actividad_form': actividad_form})


# Vista para las Actividades
def listarActividad(request):
	actividades = Actividad.objects.order_by('-fecha_realizacion')

	lista = []

	for ac in actividades:

		agencia = Agencia.objects.get(codigo_agencia = ac.codigo_agencia)
		nombre_agencia = agencia.nombre_agencia

		dic = {	'id_actividad': ac.id_actividad,
				'nombre_agencia': nombre_agencia, 
				'nombre_actividad': ac.nombre_actividad, 
				'descripcion_actividad': ac.descripcion_actividad, 
				'fecha_realizacion': ac.fecha_realizacion,
				'codigo_departamento': ac.codigo_departamento,
				'id_comite': ac.id_comite,
			}

		lista.append(dic)	

	contexto = {
				'lista': lista,
				'actividades': actividades,

	}


	#Mandar la consulta al template
	return render(request, 'evaluacionCliente/listar_actividad.html', contexto)


#Editar Actividades
def editarActividad(request, id_actividad):
	actividad_form = None
	error = None

	try:
		actividad = Actividad.objects.get(id_actividad = id_actividad)
		if request.method =='GET':
			actividad_form=ActividadForm(instance = actividad)
		else:
			actividad_form = ActividadForm(request.POST, instance = actividad)
			if actividad_form.is_valid():
				actividad_form.save()
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_actividad'))
	except ObjectDoesNotExist as e:
		error = e
	return render(request, 'evaluacionCliente/editar_actividad.html', {'actividad_form': actividad_form, 'error':error})


#Eliminar Actividad
class eliminarActividad(DeleteView):
    model = Actividad
    template_name = 'evaluacionCliente/listar_actividad.html'
    success_url = reverse_lazy('evaluacionCliente:listar_actividad')

#----------------------------------------------------------------------------------------------------------------------------------


#	CRUD EMPLEADOS

# Crear Empleado
def crearEmpleado(request):
	if request.method == 'POST':
		empleado_form = EmpleadoForm(request.POST)
		if empleado_form.is_valid():
			empleado_form.save()
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_empleados'))  
	else:
		empleado_form = EmpleadoForm()
	return render(request, 'evaluacionCliente/crear_empleado.html', {'empleado_form' : empleado_form})

# Vista para los Empleados
def listarEmpleados(request):
	empleados = Empleado.objects.order_by('nombres')
	
	# Se usa doble subrayado para que funcione como el "." en el template (osea un join)
	agencias = Agencia.objects.order_by('nombre_agencia')	
	departamentos = Departamento.objects.order_by('codigo_departamento')	
	comites = Comite.objects.order_by('nombre_comite')

	lista = []

	for emp in empleados:

		agencia = Agencia.objects.get(codigo_agencia = emp.codigo_agencia)
		nombre_agencia = agencia.nombre_agencia

		dic = {	'id_empleado': emp.id_empleado,
				'nombre_agencia': nombre_agencia, 
				'codigo_departamento': emp.codigo_departamento, 
				'id_comite': emp.id_comite, 
				'email': emp.email,
				'nombres': emp.nombres,
				'apellidos': emp.apellidos,
			}

		lista.append(dic)		
	
	context = {
	    'empleados': empleados,
	    'agencias': agencias,
	    'departamentos': departamentos,
	    'comites': comites,
	    'lista': lista
	}

	#Mandar la consulta al template
	return render(
		request, 
		'evaluacionCliente/listar_empleados.html', 
		context,	
	)

#Editar Empleado
def editarEmpleado(request, id_empleado):
	empleado_form = None
	error = None

	try:
		empleado = Empleado.objects.get(id_empleado = id_empleado)
		if request.method =='GET':
			empleado_form=EmpleadoForm(instance = empleado)
		else:
			empleado_form = EmpleadoForm(request.POST, instance = empleado)
			if empleado_form.is_valid():
				empleado_form.save()
			else:
				empleado_form = EmpleadoForm(request.POST, instance = empleado)
				return render(request, 'evaluacionCliente/editar_empleado.html', {'empleado_form': empleado_form, 'error':error})
			return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_empleados'))
	except ObjectDoesNotExist as e:
		error = e
	return render(request, 'evaluacionCliente/editar_empleado.html', {'empleado_form': empleado_form, 'error':error})


#Eliminar Empleado
class eliminarEmpleado(DeleteView):
    model = Empleado
    template_name = 'evaluacionCliente/listar_empleados.html'
    success_url = reverse_lazy('evaluacionCliente:listar_empleados')


def filtrarEmpleados(request):

	if request.method == 'POST':
		agencia = request.POST['agency']
		departamento = request.POST['depto']
		comite = request.POST['comit']

		if agencia == '':
			agencia = 'vacio'
		
		if departamento == '':
			departamento = 'vacio'

		if comite == '':
			str(comite)
			comite = 'vacio'			

		if agencia != 'vacio' and departamento != 'vacio' and comite != 'vacio':
			empleados_todos_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento, id_comite=int(comite))
			empleados_filtro=empleados_todos_filtro

		elif agencia != 'vacio' and departamento != 'vacio' :
			empleados_agencia_depto_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento)
			empleados_filtro=empleados_agencia_depto_filtro
		
		elif agencia != 'vacio' and comite != 'vacio':
			empleados_agencia_comite_filtro = Empleado.objects.filter(codigo_agencia=agencia, id_comite=int(comite))
			empleados_filtro=empleados_agencia_comite_filtro							

		elif departamento != 'vacio' and comite != 'vacio':
			empleados_depto_comite_filtro = Empleado.objects.filter(codigo_departamento=departamento, id_comite=int(comite))
			empleados_filtro=empleados_depto_comite_filtro

		elif comite !='vacio':
			empleados_comite_filtro = Empleado.objects.filter(id_comite=int(comite))
			empleados_filtro=empleados_comite_filtro

		elif agencia != 'vacio':
			empleados_agencia_filtro = Empleado.objects.filter(codigo_agencia=agencia)
			empleados_filtro=empleados_agencia_filtro

		elif departamento != 'vacio':
			empleados_depto_filtro = Empleado.objects.filter(codigo_departamento=departamento)
			empleados_filtro=empleados_depto_filtro

		elif agencia == 'vacio' and departamento == 'vacio' and comite == 'vacio':
			empleados_sin_filtro = Empleado.objects.order_by('nombres')
			empleados_filtro=empleados_sin_filtro

		agencias = Agencia.objects.order_by('nombre_agencia')	
		departamentos = Departamento.objects.order_by('codigo_departamento')	
		comites = Comite.objects.order_by('nombre_comite')	

		lista = []

		for emp in empleados_filtro:

			agenciaCod = Agencia.objects.get(codigo_agencia = emp.codigo_agencia)
			nombre_agencia = agenciaCod.nombre_agencia

			dic = {	'id_empleado': emp.id_empleado,
					'nombre_agencia': nombre_agencia, 
					'codigo_departamento': emp.codigo_departamento, 
					'id_comite': emp.id_comite, 
					'email': emp.email,
					'nombres': emp.nombres,
					'apellidos': emp.apellidos,
				}

			lista.append(dic)			

		context = {
			'lista': lista,
			'empleados_filtro': empleados_filtro,
			
			'agencia': agencia,
			'departamento': departamento,
			'comite': comite,
			
			'agencias': agencias,
			'departamentos': departamentos,
			'comites': comites,
		}

		return render(
			request,
			'evaluacionCliente/listar_empleados.html', 
			context,
		) 

def reporteEmpleadosPDF(request, agencia, departamento, comite):

	if agencia != 'vacio' and departamento !='vacio' and comite != 'vacio':
		empleados_todos_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento, id_comite=int(comite))
		reporte_empleados_filtro=empleados_todos_filtro

	elif agencia != 'vacio' and departamento != 'vacio':
		empleados_agencia_depto_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento)
		reporte_empleados_filtro=empleados_agencia_depto_filtro
	
	elif agencia != 'vacio' and comite != 'vacio':
		empleados_agencia_comite_filtro = Empleado.objects.filter(codigo_agencia=agencia, id_comite=int(comite))
		reporte_empleados_filtro=empleados_agencia_comite_filtro							

	elif departamento != 'vacio' and comite != 'vacio':
		empleados_depto_comite_filtro = Empleado.objects.filter(codigo_departamento=departamento, id_comite=int(comite))
		reporte_empleados_filtro=empleados_depto_comite_filtro

	elif comite != 'vacio':
		empleados_comite_filtro = Empleado.objects.filter(id_comite=int(comite))
		reporte_empleados_filtro=empleados_comite_filtro

	elif agencia !='vacio':
		empleados_agencia_filtro = Empleado.objects.filter(codigo_agencia=agencia)
		reporte_empleados_filtro=empleados_agencia_filtro

	elif departamento != 'vacio':
		empleados_depto_filtro = Empleado.objects.filter(codigo_departamento=departamento)
		reporte_empleados_filtro=empleados_depto_filtro

	elif agencia == 'vacio' and departamento == 'vacio' and comite == 'vacio':		
		empleados_sin_filtro = Empleado.objects.order_by('nombres')
		reporte_empleados_filtro=empleados_sin_filtro

	lista = []

	for emp in reporte_empleados_filtro:

		agenciaCod = Agencia.objects.get(codigo_agencia = emp.codigo_agencia)
		nombre_agencia = agenciaCod.nombre_agencia

		dic = {	'id_empleado': emp.id_empleado,
				'nombre_agencia': nombre_agencia, 
				'codigo_departamento': emp.codigo_departamento, 
				'id_comite': emp.id_comite, 
				'email': emp.email,
				'nombres': emp.nombres,
				'apellidos': emp.apellidos,
			}

		lista.append(dic)		


	template = get_template('reportes/ReporteEmpleados.html')

	context = {
		'lista': lista,
		'reporte_empleados_filtro': reporte_empleados_filtro
	}

	html = template.render(context)

	response = HttpResponse(content_type = 'application/pdf')
	response['Content-Disposition'] = 'inline; filename="ReportesEmpleados.pdf"'

	pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
    
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>'+ html + '</pre>')

	return response

def exportarEmpleados(request, agencia, departamento, comite):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="ReporteEmpleados.csv"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Reporte de Empleados') 

	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Nombres', 'Apellidos', 'Agencia', 'Departamento', 'Cómite', 'Correo']

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style) 

	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	if agencia != 'vacio' and departamento !='vacio' and comite != 'vacio':
		empleados_todos_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento, id_comite=int(comite))
		reporte_empleados_filtro=empleados_todos_filtro

	elif agencia != 'vacio' and departamento != 'vacio':
		empleados_agencia_depto_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento)
		reporte_empleados_filtro=empleados_agencia_depto_filtro
	
	elif agencia != 'vacio' and comite != 'vacio':
		empleados_agencia_comite_filtro = Empleado.objects.filter(codigo_agencia=agencia, id_comite=int(comite))
		reporte_empleados_filtro=empleados_agencia_comite_filtro							

	elif departamento != 'vacio' and comite != 'vacio':
		empleados_depto_comite_filtro = Empleado.objects.filter(codigo_departamento=departamento, id_comite=int(comite))
		reporte_empleados_filtro=empleados_depto_comite_filtro

	elif comite != 'vacio':
		empleados_comite_filtro = Empleado.objects.filter(id_comite=int(comite))
		reporte_empleados_filtro=empleados_comite_filtro

	elif agencia !='vacio':
		empleados_agencia_filtro = Empleado.objects.filter(codigo_agencia=agencia)
		reporte_empleados_filtro=empleados_agencia_filtro

	elif departamento != 'vacio':
		empleados_depto_filtro = Empleado.objects.filter(codigo_departamento=departamento)
		reporte_empleados_filtro=empleados_depto_filtro

	elif agencia == 'vacio' and departamento == 'vacio' and comite == 'vacio':		
		empleados_sin_filtro = Empleado.objects.order_by('nombres')
		reporte_empleados_filtro=empleados_sin_filtro

	agencias = Agencia.objects.order_by('nombre_agencia')	
	departamentos = Departamento.objects.order_by('codigo_departamento')	
	comites = Comite.objects.order_by('nombre_comite')			

	for repEmp in reporte_empleados_filtro:
		row_num += 1

		for age in agencias:			
			if repEmp.codigo_agencia_id == age.codigo_agencia:
				codAgencia= age.nombre_agencia

		for dep in departamentos:			
			if repEmp.codigo_departamento_id == dep.codigo_departamento:
				codDepto= dep.nombre_departamento

		for com in comites:			
			if repEmp.id_comite_id == com.id_comite:
				codComite = com.nombre_comite

		row = [repEmp.nombres, repEmp.apellidos, codAgencia, codDepto, codComite, repEmp.email]

		for col_num in range(len(row)):
		    ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)

	return response


#Enviar correo de Invitacion 
def enviarEmail(request, agencia, departamento, comite):
	if request.method == 'POST':
		actividad = request.POST['activity']
		cuerpoMensaje = request.POST['bodyCorreo']

		filtro_actividad = Actividad.objects.filter(id_actividad=actividad)

		for fil in filtro_actividad:
			nombreAc = fil.nombre_actividad
			fecha = fil.fecha_realizacion

		if agencia == '':
			agencia = 'vacio'
		
		if departamento == '':
			departamento = 'vacio'

		if comite == '':
			str(comite)
			comite = 'vacio'			

		if agencia != 'vacio' and departamento != 'vacio' and comite != 'vacio':
			empleados_todos_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento, id_comite=int(comite))
			empleados_filtro=empleados_todos_filtro

		elif agencia != 'vacio' and departamento != 'vacio' :
			empleados_agencia_depto_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento)
			empleados_filtro=empleados_agencia_depto_filtro
		
		elif agencia != 'vacio' and comite != 'vacio':
			empleados_agencia_comite_filtro = Empleado.objects.filter(codigo_agencia=agencia, id_comite=int(comite))
			empleados_filtro=empleados_agencia_comite_filtro							

		elif departamento != 'vacio' and comite != 'vacio':
			empleados_depto_comite_filtro = Empleado.objects.filter(codigo_departamento=departamento, id_comite=int(comite))
			empleados_filtro=empleados_depto_comite_filtro

		elif comite !='vacio':
			empleados_comite_filtro = Empleado.objects.filter(id_comite=int(comite))
			empleados_filtro=empleados_comite_filtro

		elif agencia != 'vacio':
			empleados_agencia_filtro = Empleado.objects.filter(codigo_agencia=agencia)
			empleados_filtro=empleados_agencia_filtro

		elif departamento != 'vacio':
			empleados_depto_filtro = Empleado.objects.filter(codigo_departamento=departamento)
			empleados_filtro=empleados_depto_filtro

		elif agencia == 'vacio' and departamento == 'vacio' and comite == 'vacio':
			empleados_sin_filtro = Empleado.objects.order_by('nombres')
			empleados_filtro=empleados_sin_filtro
		
		for ite in empleados_filtro:
			try:
				# Establecemos conexion con el servidor smtp de gmail
				mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
				print(mailServer.ehlo())
				mailServer.starttls()
				print(mailServer.ehlo())
				mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
				print('...Conectado')

				# Construimos el mensaje
				mensaje = MIMEMultipart()
				mensaje['From']= settings.EMAIL_HOST_USER
				mensaje['To']= ite.email
				print(ite.email)
				mensaje['Subject']="Invitacion a la actividad de: " + nombreAc
				print(nombreAc)

				context = {
					'nombres': ite.nombres,
					'actividad': nombreAc,
					'fecha': fecha,
					'cuerpoMensaje': cuerpoMensaje,
				}

				content = render_to_string('accounts/plantilla_correo.html', context)

				# Adjuntamos el texto
				mensaje.attach(MIMEText(content, 'html'))		

				# Envio del mensaje
				mailServer.sendmail(settings.EMAIL_HOST_USER,
				                ite.email,
				                mensaje.as_string())

				print('Correo enviado correctamente')		

			except Exception as e:
				print(e)

	return HttpResponseRedirect(reverse_lazy('evaluacionCliente:confirmar_invitacion'))  

def confirmarInvitacion(request):
	return render(
		request, 
		'evaluacionCliente/confirmar_invitacion.html', 
	)	

# Vista para los Empleados
def listarEmpleadosCorreo(request):
	empleados = Empleado.objects.order_by('nombres')
	
	# Se usa doble subrayado para que funcione como el "." en el template (osea un join)
	agencias = Agencia.objects.order_by('nombre_agencia')	
	departamentos = Departamento.objects.order_by('codigo_departamento')	
	comites = Comite.objects.order_by('nombre_comite')	
	
	context = {
	    'empleados': empleados,
	    'agencias': agencias,
	    'departamentos': departamentos,
	    'comites': comites,
	}

	#Mandar la consulta al template
	return render(
		request, 
		'evaluacionCliente/listar_empleados_correo.html', 
		context,	
	)	

def filtrarEmpleadosCorreo(request):

	if request.method == 'POST':
		agencia = request.POST['agency']
		departamento = request.POST['depto']
		comite = request.POST['comit']

		if agencia == '':
			agencia = 'vacio'
		
		if departamento == '':
			departamento = 'vacio'

		if comite == '':
			str(comite)
			comite = 'vacio'			

		if agencia != 'vacio' and departamento != 'vacio' and comite != 'vacio':
			empleados_todos_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento, id_comite=int(comite))
			empleados_filtro=empleados_todos_filtro

		elif agencia != 'vacio' and departamento != 'vacio' :
			empleados_agencia_depto_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento)
			empleados_filtro=empleados_agencia_depto_filtro
		
		elif agencia != 'vacio' and comite != 'vacio':
			empleados_agencia_comite_filtro = Empleado.objects.filter(codigo_agencia=agencia, id_comite=int(comite))
			empleados_filtro=empleados_agencia_comite_filtro							

		elif departamento != 'vacio' and comite != 'vacio':
			empleados_depto_comite_filtro = Empleado.objects.filter(codigo_departamento=departamento, id_comite=int(comite))
			empleados_filtro=empleados_depto_comite_filtro

		elif comite !='vacio':
			empleados_comite_filtro = Empleado.objects.filter(id_comite=int(comite))
			empleados_filtro=empleados_comite_filtro

		elif agencia != 'vacio':
			empleados_agencia_filtro = Empleado.objects.filter(codigo_agencia=agencia)
			empleados_filtro=empleados_agencia_filtro

		elif departamento != 'vacio':
			empleados_depto_filtro = Empleado.objects.filter(codigo_departamento=departamento)
			empleados_filtro=empleados_depto_filtro

		elif agencia == 'vacio' and departamento == 'vacio' and comite == 'vacio':
			empleados_sin_filtro = Empleado.objects.order_by('nombres')
			empleados_filtro=empleados_sin_filtro

		agencias = Agencia.objects.order_by('nombre_agencia')	
		departamentos = Departamento.objects.order_by('codigo_departamento')	
		comites = Comite.objects.order_by('nombre_comite')	

		context = {
			'empleados_filtro': empleados_filtro,
			
			'agencia': agencia,
			'departamento': departamento,
			'comite': comite,
			
			'agencias': agencias,
			'departamentos': departamentos,
			'comites': comites,
		}

		return render(
			request,
			'evaluacionCliente/listar_empleados_correo.html', 
			context,
		) 

def enviarCorreo(request, agencia, departamento, comite):

	actividad = Actividad.objects.order_by('-fecha_realizacion')	

	if agencia != 'vacio' and departamento !='vacio' and comite != 'vacio':
		empleados_todos_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento, id_comite=int(comite))
		reporte_empleados_filtro=empleados_todos_filtro

	elif agencia != 'vacio' and departamento != 'vacio':
		empleados_agencia_depto_filtro = Empleado.objects.filter(codigo_agencia=agencia, codigo_departamento=departamento)
		reporte_empleados_filtro=empleados_agencia_depto_filtro
	
	elif agencia != 'vacio' and comite != 'vacio':
		empleados_agencia_comite_filtro = Empleado.objects.filter(codigo_agencia=agencia, id_comite=int(comite))
		reporte_empleados_filtro=empleados_agencia_comite_filtro							

	elif departamento != 'vacio' and comite != 'vacio':
		empleados_depto_comite_filtro = Empleado.objects.filter(codigo_departamento=departamento, id_comite=int(comite))
		reporte_empleados_filtro=empleados_depto_comite_filtro

	elif comite != 'vacio':
		empleados_comite_filtro = Empleado.objects.filter(id_comite=int(comite))
		reporte_empleados_filtro=empleados_comite_filtro

	elif agencia !='vacio':
		empleados_agencia_filtro = Empleado.objects.filter(codigo_agencia=agencia)
		reporte_empleados_filtro=empleados_agencia_filtro

	elif departamento != 'vacio':
		empleados_depto_filtro = Empleado.objects.filter(codigo_departamento=departamento)
		reporte_empleados_filtro=empleados_depto_filtro

	elif agencia == 'vacio' and departamento == 'vacio' and comite == 'vacio':		
		empleados_sin_filtro = Empleado.objects.order_by('nombres')
		reporte_empleados_filtro=empleados_sin_filtro
		
	context = {

		'actividad': actividad,

		'reporte_empleados_filtro': reporte_empleados_filtro,
		
		'agencia': agencia,
		'departamento': departamento,
		'comite': comite,
	}

	return render(
		request,
		'evaluacionCliente/enviar_correo.html', 
		context,
	) 

#----------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------------------------------------------------
#								ESTA PARTE ES PARA LA ENCUESTA DEL CLIENTE
#----------------------------------------------------------------------------------------------------------------------------------


def crearEncuesta(request, codigoAgencia):
	if request.method == 'POST':
		titulo = request.POST['titulo']
		pregunta = request.POST['pregunta']
		visibilidad = request.POST['visibilidad']
		fechaDesde = request.POST['fecha_desde']
		fechaHasta = request.POST['fecha_hasta']
		agencia = codigoAgencia

		if fechaHasta == "":
			encuestaCliente = EncuestaCliente(codigo_agencia_id=agencia, descripcion_pregunta=pregunta, titulo_encuesta_cliente=titulo, visibilidad_pregunta_cliente=visibilidad, fecha_desde_cliente=fechaDesde)
		else:
			encuestaCliente = EncuestaCliente(codigo_agencia_id=agencia, descripcion_pregunta=pregunta, titulo_encuesta_cliente=titulo, visibilidad_pregunta_cliente=visibilidad, fecha_desde_cliente=fechaDesde, fecha_hasta_cliente=fechaHasta)
		
		encuestaCliente.save()

		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2', kwargs={'codigoAgencia':agencia, 'tituloEncuesta':titulo}))
	
	else:
		codigoAgencia = codigoAgencia
		agen = Agencia.objects.filter(codigo_agencia = codigoAgencia)

		context = {
			'agen' : agen,
			'codigoAgencia' : codigoAgencia,
		}

		return render(
			request,
			'evaluacionCliente/crear_encuesta_cliente.html', 
			context
		)


#----------------------------------------------------------------------------------------------------------------------------------


def editarEncuesta(request, idEncuesta):
	if request.method == 'POST':
		pregunta = request.POST['pregunta']
		visibilidad = request.POST['visibilidad']
		idEnc = idEncuesta
		enc = EncuestaCliente.objects.filter(id=idEnc)

		i=0
		while i < len(enc):
			agencia = enc[i].codigo_agencia
			titulo = enc[i].titulo_encuesta_cliente
			desde = enc[i].fecha_desde_cliente
			hasta = enc[i].fecha_hasta_cliente
			i+=1

		encuestaCliente = EncuestaCliente(id=idEnc, codigo_agencia_id=agencia, descripcion_pregunta=pregunta, titulo_encuesta_cliente=titulo, visibilidad_pregunta_cliente=visibilidad, fecha_desde_cliente=desde, fecha_hasta_cliente=hasta)
		
		encuestaCliente.save()

		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2', kwargs={'codigoAgencia':agencia, 'tituloEncuesta':titulo}))
	
	else:
		idEnc = idEncuesta
		enc = EncuestaCliente.objects.filter(id=idEnc)

		i=0
		while i < len(enc):
			agencia = enc[i].codigo_agencia
			titulo = enc[i].titulo_encuesta_cliente
			i+=1

		encuesta = EncuestaCliente.objects.filter(id=idEnc)

		context = {
			'idEnc': idEnc,
			'encuesta' : encuesta,
			'codigoAgencia': agencia,
			'tituloEncuesta': titulo,
		}

		return render(
			request,
			'evaluacionCliente/editar_encuesta_cliente.html', 
			context
		)


#----------------------------------------------------------------------------------------------------------------------------------


def eliminarEncuesta(request, idEncuesta):
	encuesta = EncuestaCliente.objects.filter(id=idEncuesta)

	i=0
	while i < len(encuesta):
		agencia = encuesta[i].codigo_agencia
		titulo = encuesta[i].titulo_encuesta_cliente
		i+=1

	EncuestaCliente.objects.get(id=idEncuesta).delete()

	encuestaVal = EncuestaCliente.objects.filter(titulo_encuesta_cliente = titulo, codigo_agencia=agencia)

	if len(encuestaVal) == 0:
		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_encuesta'))
	
	else:
		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2', kwargs={'codigoAgencia':agencia, 'tituloEncuesta':titulo}))


#----------------------------------------------------------------------------------------------------------------------------------


def editarInfEncuesta(request, idEncuesta):
	if request.method == 'POST':
		tituloN = request.POST['titulo']
		desdeN = request.POST['desde']
		hastaN = request.POST['hasta']
		idEnc = idEncuesta
		enc = EncuestaCliente.objects.filter(id=idEnc)

		i=0
		while i < len(enc):
			agencia = enc[i].codigo_agencia
			titulo = enc[i].titulo_encuesta_cliente
			i+=1

		encuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = agencia, titulo_encuesta_cliente = titulo)
		
		if desdeN == "" and hastaN == "":
			j=0
			while j < len(encuestasClientes):
				idEnCl = encuestasClientes[j].id
				descripcion = encuestasClientes[j].descripcion_pregunta
				visibilidad = encuestasClientes[j].visibilidad_pregunta_cliente
				desde = encuestasClientes[j].fecha_desde_cliente
				hasta = encuestasClientes[j].fecha_hasta_cliente

				encuestaCliente = EncuestaCliente(id=idEnCl, codigo_agencia_id=agencia, descripcion_pregunta=descripcion, titulo_encuesta_cliente=tituloN, visibilidad_pregunta_cliente=visibilidad, fecha_desde_cliente=desde, fecha_hasta_cliente=hasta)
				encuestaCliente.save()

				j+=1

		elif desdeN != "" and hastaN == "":
			j=0
			while j < len(encuestasClientes):
				idEnCl = encuestasClientes[j].id
				descripcion = encuestasClientes[j].descripcion_pregunta
				visibilidad = encuestasClientes[j].visibilidad_pregunta_cliente
				hasta = encuestasClientes[j].fecha_hasta_cliente

				encuestaCliente = EncuestaCliente(id=idEnCl, codigo_agencia_id=agencia, descripcion_pregunta=descripcion, titulo_encuesta_cliente=tituloN, visibilidad_pregunta_cliente=visibilidad, fecha_desde_cliente=desdeN, fecha_hasta_cliente=hasta)
				encuestaCliente.save()

				j+=1

		elif desdeN == "" and hastaN != "":
			j=0
			while j < len(encuestasClientes):
				idEnCl = encuestasClientes[j].id
				descripcion = encuestasClientes[j].descripcion_pregunta
				visibilidad = encuestasClientes[j].visibilidad_pregunta_cliente
				desde = encuestasClientes[j].fecha_desde_cliente

				encuestaCliente = EncuestaCliente(id=idEnCl, codigo_agencia_id=agencia, descripcion_pregunta=descripcion, titulo_encuesta_cliente=tituloN, visibilidad_pregunta_cliente=visibilidad, fecha_desde_cliente=desde, fecha_hasta_cliente=hastaN)
				encuestaCliente.save()

				j+=1

		else:
			j=0
			while j < len(encuestasClientes):
				idEnCl = encuestasClientes[j].id
				descripcion = encuestasClientes[j].descripcion_pregunta
				visibilidad = encuestasClientes[j].visibilidad_pregunta_cliente

				encuestaCliente = EncuestaCliente(id=idEnCl, codigo_agencia_id=agencia, descripcion_pregunta=descripcion, titulo_encuesta_cliente=tituloN, visibilidad_pregunta_cliente=visibilidad, fecha_desde_cliente=desdeN, fecha_hasta_cliente=hastaN)
				encuestaCliente.save()

				j+=1

		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2', kwargs={'codigoAgencia':agencia, 'tituloEncuesta':tituloN}))
	
	else:
		idEnc = idEncuesta
		enc = EncuestaCliente.objects.filter(id=idEnc)

		i=0
		while i < len(enc):
			agencia = enc[i].codigo_agencia
			titulo = enc[i].titulo_encuesta_cliente
			i+=1

		encuesta = EncuestaCliente.objects.filter(id=idEnc)

		context = {
			'idEnc': idEnc,
			'encuesta' : encuesta,
			'codigoAgencia': agencia,
			'tituloEncuesta': titulo,
		}

		return render(
			request,
			'evaluacionCliente/editar_inf_encuesta_cliente.html', 
			context
		)


#----------------------------------------------------------------------------------------------------------------------------------


# LISTAR Agencias para buscar ENCUESTA
def listarEncuesta(request):
	agencias = Agencia.objects.all()

	context = {
		'agenciasCon': agencias,
	}

	return render(
		request,
		'evaluacionCliente/listar_encuesta.html',
		context
	)


#----------------------------------------------------------------------------------------------------------------------------------


# Mostrar la Encuesta de esa Agencia
def consultarAgencia(request):
	if request.method == 'POST':
		codigo_agencia = request.POST['codigo_agencia']
		
		encuestasAgencia = EncuestaCliente.objects.raw('select id, titulo_encuesta_cliente from proyecto_encuestacliente where codigo_agencia_id = %s group by titulo_encuesta_cliente;', [codigo_agencia])
		nombreAgencia = Agencia.objects.filter(codigo_agencia = codigo_agencia)

		i=0
		while i < len(nombreAgencia):
			codAgencia = nombreAgencia[i].codigo_agencia
			i+=1
		
		contexto = {
			'encuestasAgencia': encuestasAgencia,
			'nombreAgencia': nombreAgencia,
			'codAgencia': codAgencia,
			'codigo_agencia': codigo_agencia,
		}
			
		return render(
			request, 
			'evaluacionCliente/listar_encuesta.html', 
			contexto
			)



# Mostrar la Encuesta de esa Agencia
def consultarAgencia2(request, codigoAgencia):
	codigo_agencia = codigoAgencia
	
	encuestasAgencia = EncuestaCliente.objects.raw('select id, titulo_encuesta_cliente from proyecto_encuestacliente where codigo_agencia_id = %s group by titulo_encuesta_cliente;', [codigo_agencia])
	nombreAgencia = Agencia.objects.filter(codigo_agencia = codigo_agencia)

	i=0
	while i < len(nombreAgencia):
		codAgencia = nombreAgencia[i].codigo_agencia
		i+=1
	
	contexto = {
		'encuestasAgencia': encuestasAgencia,
		'nombreAgencia': nombreAgencia,
		'codAgencia': codAgencia,
		'codigo_agencia': codigo_agencia,
	}
		
	return render(
		request, 
		'evaluacionCliente/listar_encuesta.html', 
		contexto
		)


#----------------------------------------------------------------------------------------------------------------------------------


# Mostrar la Encuesta de esa Agencia
def consultarEncuesta(request, codigoAgencia):
	if request.method == 'POST':
		titulo_encuesta = request.POST['titulo_encuesta']
		codigo_agencia = codigoAgencia

		encuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta)
		
		encuestas = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia)
		agencias = Agencia.objects.all()

		i=0
		while i<1:
			tituloEncuesta = encuestasClientes[i].titulo_encuesta_cliente
			nombreAgencia = encuestasClientes[i].codigo_agencia.nombre_agencia
			desde = encuestasClientes[i].fecha_desde_cliente
			hasta = encuestasClientes[i].fecha_hasta_cliente
			idCl = encuestasClientes[i].id
			i+=1

		contexto = {
			'encuestasClientes': encuestasClientes,
			'agencias': agencias,
			'encuestas': encuestas,
			'nombreAgencia' : nombreAgencia,
			'tituloEncuesta' : tituloEncuesta,
			'codigoAgencia' : codigo_agencia,
			'desde' : desde,
			'hasta' : hasta,
			'idCl' : idCl,
		}
			
		return render(
			request, 
			'evaluacionCliente/listar_encuesta.html', 
			contexto
			)



# Mostrar la Encuesta de esa Agencia (Parametros por URL al dar cancelar)
def consultarEncuesta2(request, codigoAgencia, tituloEncuesta):
	titulo_encuesta = tituloEncuesta
	codigo_agencia = codigoAgencia

	encuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta)
	
	encuestas = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia)
	agencias = Agencia.objects.all()

	i=0
	while i<1:
		tituloEncuesta = encuestasClientes[i].titulo_encuesta_cliente
		nombreAgencia = encuestasClientes[i].codigo_agencia.nombre_agencia
		desde = encuestasClientes[i].fecha_desde_cliente
		hasta = encuestasClientes[i].fecha_hasta_cliente
		idCl = encuestasClientes[i].id
		i+=1

	contexto = {
		'encuestasClientes': encuestasClientes,
		'agencias': agencias,
		'encuestas': encuestas,
		'nombreAgencia' : nombreAgencia,
		'tituloEncuesta' : tituloEncuesta,
		'codigoAgencia' : codigo_agencia,
		'desde' : desde,
		'hasta' : hasta,
		'idCl' : idCl,
	}
		
	return render(
		request, 
		'evaluacionCliente/listar_encuesta.html', 
		contexto
		)


#----------------------------------------------------------------------------------------------------------------------------------


# Agregar Preguntas a la Encuesta
def AgregarPreguntasEncuestaCliente(request, codigoAgencia, tituloEncuesta):
	if request.method == 'POST':
		pregunta = request.POST['pregunta']
		visibilidad = request.POST['visibilidad']
		agencia = codigoAgencia
		titulo = tituloEncuesta

		encues = EncuestaCliente.objects.filter(codigo_agencia=agencia, titulo_encuesta_cliente=titulo)
		i=0
		while i < 1:
			desde = encues[i].fecha_desde_cliente
			hasta = encues[i].fecha_hasta_cliente
			i+=1

		encuestaCliente = EncuestaCliente(codigo_agencia_id=agencia, descripcion_pregunta=pregunta, titulo_encuesta_cliente=titulo, visibilidad_pregunta_cliente=visibilidad, fecha_desde_cliente=desde, fecha_hasta_cliente=hasta)
		
		encuestaCliente.save()

		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2', kwargs={'codigoAgencia':agencia, 'tituloEncuesta':titulo}))
	
	else:
		codigoAgencia = codigoAgencia
		tituloEncuesta = tituloEncuesta
		agen = Agencia.objects.filter(codigo_agencia = codigoAgencia)

		context = {
			'agen' : agen,
			'codigoAgencia' : codigoAgencia,
			'tituloEncuesta' : tituloEncuesta,
		}

		return render(
			request,
			'evaluacionCliente/agregar_preguntas_encuesta_cliente.html', 
			context
		)



#----------------------------------------------------------------------------------------------------------------------------------
#								ESTA PARTE ES PARA LA ENCUESTA DEL PERSONAL
#----------------------------------------------------------------------------------------------------------------------------------



def crearEncuestaPersonal(request, idActividad):
	if request.method == 'POST':
		titulo = request.POST['titulo']
		pregunta = request.POST['pregunta']
		visibilidad = request.POST['visibilidad']
		fechaDesde = request.POST['fecha_desde']
		fechaHasta = request.POST['fecha_hasta']
		actividad = idActividad

		if fechaHasta == "":
			encuestaPersonal = EncuestaPersonal(id_actividad_id=actividad, descripcion_pregunta=pregunta, titulo_encuesta_personal=titulo, visibilidad_pregunta_personal=visibilidad, fecha_desde_personal=fechaDesde)
		else:
			encuestaPersonal = EncuestaPersonal(id_actividad_id=actividad, descripcion_pregunta=pregunta, titulo_encuesta_personal=titulo, visibilidad_pregunta_personal=visibilidad, fecha_desde_personal=fechaDesde, fecha_hasta_personal=fechaHasta)
		
		encuestaPersonal.save()

		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2_personal', kwargs={'idActividad':actividad, 'tituloEncuesta':titulo}))
	
	else:
		codigoActividad = idActividad
		act = Actividad.objects.filter(id_actividad = codigoActividad)

		context = {
			'act' : act,
			'codigoActividad' : codigoActividad,
		}

		return render(
			request,
			'evaluacionCliente/crear_encuesta_personal.html', 
			context
		)


#----------------------------------------------------------------------------------------------------------------------------------


def editarEncuestaPersonal(request, idEncuesta):
	if request.method == 'POST':
		pregunta = request.POST['pregunta']
		visibilidad = request.POST['visibilidad']
		idEnc = idEncuesta
		enc = EncuestaPersonal.objects.filter(id=idEnc)

		i=0
		while i < len(enc):
			actividad = enc[i].id_actividad.id_actividad
			titulo = enc[i].titulo_encuesta_personal
			desde = enc[i].fecha_desde_personal
			hasta = enc[i].fecha_hasta_personal
			i+=1
		
		encuestaPersonal = EncuestaPersonal(id=idEnc, id_actividad_id=actividad, descripcion_pregunta=pregunta, titulo_encuesta_personal=titulo, visibilidad_pregunta_personal=visibilidad, fecha_desde_personal=desde, fecha_hasta_personal=hasta)
		
		encuestaPersonal.save()

		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2_personal', kwargs={'idActividad':actividad, 'tituloEncuesta':titulo}))
	
	else:
		idEnc = idEncuesta
		enc = EncuestaPersonal.objects.filter(id=idEnc)

		i=0
		while i < len(enc):
			actividad = enc[i].id_actividad.id_actividad
			titulo = enc[i].titulo_encuesta_personal
			i+=1

		encuesta = EncuestaPersonal.objects.filter(id=idEnc)

		context = {
			'idEnc': idEnc,
			'encuesta' : encuesta,
			'codigoActividad': actividad,
			'tituloEncuesta': titulo,
		}

		return render(
			request,
			'evaluacionCliente/editar_encuesta_personal.html', 
			context
		)


#----------------------------------------------------------------------------------------------------------------------------------


def eliminarEncuestaPersonal(request, idEncuesta):
	encuesta = EncuestaPersonal.objects.filter(id=idEncuesta)

	i=0
	while i < len(encuesta):
		actividad = encuesta[i].id_actividad.id_actividad
		titulo = encuesta[i].titulo_encuesta_personal
		i+=1
	
	EncuestaPersonal.objects.get(id=idEncuesta).delete()

	encuestaVal = EncuestaPersonal.objects.filter(id_actividad=actividad, titulo_encuesta_personal=titulo)

	if len(encuestaVal) == 0:
		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:listar_encuesta_personal'))
	
	else:
		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2_personal', kwargs={'idActividad':actividad, 'tituloEncuesta':titulo}))


#----------------------------------------------------------------------------------------------------------------------------------


def editarInfEncuestaPersonal(request, idEncuesta):
	if request.method == 'POST':
		tituloN = request.POST['titulo']
		desdeN = request.POST['desde']
		hastaN = request.POST['hasta']
		idEnc = idEncuesta
		enc = EncuestaPersonal.objects.filter(id=idEnc)

		i=0
		while i < len(enc):
			actividad = enc[i].id_actividad.id_actividad
			titulo = enc[i].titulo_encuesta_personal
			i+=1

		encuestasPersonal = EncuestaPersonal.objects.filter(id_actividad_id=actividad, titulo_encuesta_personal=titulo)
		
		if desdeN == "" and hastaN == "":
			j=0
			while j < len(encuestasPersonal):
				idEnPer = encuestasPersonal[j].id
				descripcion = encuestasPersonal[j].descripcion_pregunta
				visibilidad = encuestasPersonal[j].visibilidad_pregunta_personal
				desde = encuestasPersonal[j].fecha_desde_personal
				hasta = encuestasPersonal[j].fecha_hasta_personal

				encuestaPersonal = EncuestaPersonal(id=idEnPer, id_actividad_id=actividad, descripcion_pregunta=descripcion, titulo_encuesta_personal=tituloN, visibilidad_pregunta_personal=visibilidad, fecha_desde_personal=desde, fecha_hasta_personal=hasta)
				encuestaPersonal.save()

				j+=1

		elif desdeN != "" and hastaN == "":
			j=0
			while j < len(encuestasPersonal):
				idEnPer = encuestasPersonal[j].id
				descripcion = encuestasPersonal[j].descripcion_pregunta
				visibilidad = encuestasPersonal[j].visibilidad_pregunta_personal
				hasta = encuestasPersonal[j].fecha_hasta_personal

				encuestaPersonal = EncuestaPersonal(id=idEnPer, id_actividad_id=actividad, descripcion_pregunta=descripcion, titulo_encuesta_personal=tituloN, visibilidad_pregunta_personal=visibilidad, fecha_desde_personal=desdeN, fecha_hasta_personal=hasta)
				encuestaPersonal.save()

				j+=1

		elif desdeN == "" and hastaN != "":
			j=0
			while j < len(encuestasPersonal):
				idEnPer = encuestasPersonal[j].id
				descripcion = encuestasPersonal[j].descripcion_pregunta
				visibilidad = encuestasPersonal[j].visibilidad_pregunta_personal
				desde = encuestasPersonal[j].fecha_desde_personal

				encuestaPersonal = EncuestaPersonal(id=idEnPer, id_actividad_id=actividad, descripcion_pregunta=descripcion, titulo_encuesta_personal=tituloN, visibilidad_pregunta_personal=visibilidad, fecha_desde_personal=desde, fecha_hasta_personal=hastaN)
				encuestaPersonal.save()

				j+=1

		else:
			j=0
			while j < len(encuestasPersonal):
				idEnPer = encuestasPersonal[j].id
				descripcion = encuestasPersonal[j].descripcion_pregunta
				visibilidad = encuestasPersonal[j].visibilidad_pregunta_personal

				encuestaPersonal = EncuestaPersonal(id=idEnPer, id_actividad_id=actividad, descripcion_pregunta=descripcion, titulo_encuesta_personal=tituloN, visibilidad_pregunta_personal=visibilidad, fecha_desde_personal=desdeN, fecha_hasta_personal=hastaN)
				encuestaPersonal.save()

				j+=1

		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2_personal', kwargs={'idActividad':actividad, 'tituloEncuesta':tituloN}))
	
	else:
		idEnc = idEncuesta
		enc = EncuestaPersonal.objects.filter(id=idEnc)

		i=0
		while i < len(enc):
			actividad = enc[i].id_actividad.id_actividad
			titulo = enc[i].titulo_encuesta_personal
			i+=1

		encuesta = EncuestaPersonal.objects.filter(id=idEnc)

		context = {
			'idEnc': idEnc,
			'encuesta' : encuesta,
			'codigoActividad': actividad,
			'tituloEncuesta': titulo,
		}

		return render(
			request,
			'evaluacionCliente/editar_inf_encuesta_personal.html', 
			context
		)


#----------------------------------------------------------------------------------------------------------------------------------


# LISTAR Agencias para buscar ENCUESTA
def listarEncuestaPersonal(request):
	actividades = Actividad.objects.all().order_by('codigo_agencia')

	context = {
		'actividadesCon': actividades,
	}

	return render(
		request,
		'evaluacionCliente/listar_encuesta_personal.html',
		context
	)


#----------------------------------------------------------------------------------------------------------------------------------


# Mostrar la Encuesta de esa Agencia
def consultarActividadPersonal(request):
	if request.method == 'POST':
		codigo_actividad = request.POST['codigo_actividad']
		
		encuestasActividad = EncuestaPersonal.objects.raw('select id, titulo_encuesta_personal from proyecto_encuestapersonal where id_actividad_id = %s group by titulo_encuesta_personal;', [codigo_actividad])
		nombreActividad = Actividad.objects.filter(id_actividad = codigo_actividad)
		
		i=0
		while i < len(nombreActividad):
			codActividad = nombreActividad[i].id_actividad
			i+=1
		
		contexto = {
			'encuestasActividad': encuestasActividad,
			'nombreActividad': nombreActividad,
			'codActividad': codActividad,
			'codigo_actividad': codigo_actividad,
		}
			
		return render(
			request, 
			'evaluacionCliente/listar_encuesta_personal.html', 
			contexto
			)



# Mostrar la Encuesta de esa Agencia
def consultarActividad2Personal(request, idActividad):
	codigo_actividad = idActividad
	
	encuestasActividad = EncuestaPersonal.objects.raw('select id, titulo_encuesta_personal from proyecto_encuestapersonal where id_actividad_id = %s group by titulo_encuesta_personal;', [codigo_actividad])
	nombreActividad = Actividad.objects.filter(id_actividad = codigo_actividad)

	i=0
	while i < len(nombreActividad):
		codActividad = nombreActividad[i].id_actividad
		i+=1
	
	contexto = {
		'encuestasActividad': encuestasActividad,
		'nombreActividad': nombreActividad,
		'codActividad': codActividad,
		'codigo_actividad': codigo_actividad
	}
		
	return render(
		request, 
		'evaluacionCliente/listar_encuesta_personal.html', 
		contexto
		)


#----------------------------------------------------------------------------------------------------------------------------------


# Mostrar la Encuesta de esa Agencia
def consultarEncuestaPersonal(request, idActividad):
	if request.method == 'POST':
		titulo_encuesta = request.POST['titulo_encuesta']
		codigo_actividad = idActividad

		encuestasPersonal = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad, titulo_encuesta_personal = titulo_encuesta)
		
		encuestas = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad)
		actividades = Actividad.objects.all()

		i=0
		while i<1:
			tituloEncuesta = encuestasPersonal[i].titulo_encuesta_personal
			nombreAgencia = encuestasPersonal[i].id_actividad.codigo_agencia.nombre_agencia
			nombreActividad = encuestasPersonal[i].id_actividad.nombre_actividad
			desde = encuestasPersonal[i].fecha_desde_personal
			hasta = encuestasPersonal[i].fecha_hasta_personal
			idPer = encuestasPersonal[i].id
			i+=1

		contexto = {
			'encuestasPersonal': encuestasPersonal,
			'actividades': actividades,
			'encuestas': encuestas,
			'nombreAgencia' : nombreAgencia,
			'nombreActividad' : nombreActividad,
			'tituloEncuesta' : tituloEncuesta,
			'codigoActividad' : codigo_actividad,
			'desde' : desde,
			'hasta' : hasta,
			'idPer' : idPer,
		}
			
		return render(
			request, 
			'evaluacionCliente/listar_encuesta_personal.html', 
			contexto
			)



# Mostrar la Encuesta de esa Agencia (Parametros por URL al dar cancelar)
def consultarEncuesta2Personal(request, idActividad, tituloEncuesta):
	titulo_encuesta = tituloEncuesta
	codigo_actividad = idActividad

	encuestasPersonal = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad, titulo_encuesta_personal = titulo_encuesta)
	
	encuestas = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad)
	actividades = Actividad.objects.all()

	i=0
	while i<1:
		tituloEncuesta = encuestasPersonal[i].titulo_encuesta_personal
		nombreAgencia = encuestasPersonal[i].id_actividad.codigo_agencia.nombre_agencia
		nombreActividad = encuestasPersonal[i].id_actividad.nombre_actividad
		desde = encuestasPersonal[i].fecha_desde_personal
		hasta = encuestasPersonal[i].fecha_hasta_personal
		idPer = encuestasPersonal[i].id
		i+=1

	contexto = {
		'encuestasPersonal': encuestasPersonal,
		'actividades': actividades,
		'encuestas': encuestas,
		'nombreAgencia' : nombreAgencia,
		'nombreActividad' : nombreActividad,
		'tituloEncuesta' : tituloEncuesta,
		'codigoActividad' : codigo_actividad,
		'desde' : desde,
		'hasta' : hasta,
		'idPer' : idPer,
	}
		
	return render(
		request, 
		'evaluacionCliente/listar_encuesta_personal.html', 
		contexto
		)


#----------------------------------------------------------------------------------------------------------------------------------


# Agregar Preguntas a la Encuesta
def AgregarPreguntasEncuestaPersonal(request, idActividad, tituloEncuesta):
	if request.method == 'POST':
		pregunta = request.POST['pregunta']
		visibilidad = request.POST['visibilidad']
		actividad = idActividad
		titulo = tituloEncuesta

		encues = EncuestaPersonal.objects.filter(id_actividad_id=actividad, titulo_encuesta_personal=titulo)
		i=0
		while i < 1:
			desde = encues[i].fecha_desde_personal
			hasta = encues[i].fecha_hasta_personal
			i+=1

		encuestaPersonal = EncuestaPersonal(id_actividad_id=actividad, descripcion_pregunta=pregunta, titulo_encuesta_personal=titulo, visibilidad_pregunta_personal=visibilidad, fecha_desde_personal=desde, fecha_hasta_personal=hasta)
		
		encuestaPersonal.save()

		return HttpResponseRedirect(reverse_lazy('evaluacionCliente:consultar_encuesta2_personal', kwargs={'idActividad':actividad, 'tituloEncuesta':titulo}))
	
	else:
		codigoActividad = idActividad
		tituloEncuesta = tituloEncuesta
		act = Actividad.objects.filter(id_actividad = codigoActividad)

		context = {
			'act' : act,
			'codigoActividad' : codigoActividad,
			'tituloEncuesta' : tituloEncuesta,
		}

		return render(
			request,
			'evaluacionCliente/agregar_preguntas_encuesta_personal.html', 
			context
		)


#----------------------------------------------------------------------------------------------------------------------------------


#Vista para Contestar la Encuesta
def contestarEncuesta(request):
	agencias = Agencia.objects.all()

	context = {
		'agencias': agencias,
	}
	
	return render(
        request,
        'evaluacionCliente/contestar_encuesta.html',
		context
    )


# Mostrar las Agencias
def consultarAgenciaEncuesta(request):
	if request.method == 'POST':
		codigo_agencia = request.POST['codigo_agencia']
		
		encuestasAgencia = EncuestaCliente.objects.raw('select id, titulo_encuesta_cliente from proyecto_encuestacliente where codigo_agencia_id = %s group by titulo_encuesta_cliente;', [codigo_agencia])
		nombreAgencia = Agencia.objects.filter(codigo_agencia = codigo_agencia)

		# Procedimiento para validar la Fecha Hasta y asi mostrar la encuesta o no
		fechaHoy = datetime.now().date()
		titulosEncuestas = []
		j=0
		while j < len(encuestasAgencia):
			fechaDesde = encuestasAgencia[j].fecha_desde_cliente
			fechaHasta = encuestasAgencia[j].fecha_hasta_cliente
			if (fechaHasta == None) or (fechaHasta >= fechaHoy):
				titulosEncuestas.append(encuestasAgencia[j].titulo_encuesta_cliente)
			j+=1

		i=0
		while i < len(nombreAgencia):
			codAgencia = nombreAgencia[i].codigo_agencia
			i+=1

		if len(encuestasAgencia) > 0:
			contexto = {
				'encuestasAgencia': encuestasAgencia,
				'nombreAgencia': nombreAgencia,
				'codAgencia': codAgencia,
				'codigo_agencia': codigo_agencia,
				'titulosEncuestas': titulosEncuestas,
			}

		else:
			noHayEncuestas = "NoHay"
		
			contexto = {
				'encuestasAgencia': encuestasAgencia,
				'nombreAgencia': nombreAgencia,
				'codAgencia': codAgencia,
				'codigo_agencia': codigo_agencia,
				'noHayEncuestas': noHayEncuestas,
				'titulosEncuestas': titulosEncuestas,
			}
		
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta.html', 
			contexto
			)


# Mostrar la Encuesta de esa Agencia
def consultarEncuestaCliente(request, codigoAgencia):
	if request.method == 'POST':
		titulo_encuesta = request.POST['titulo_encuesta']
		codigo_agencia = codigoAgencia

		encuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta, visibilidad_pregunta_cliente = 'S')

		if len(encuestasClientes) > 0:
			i=0
			contador = i
			while i<1:
				tituloEncuesta = encuestasClientes[i].titulo_encuesta_cliente
				nombreAgencia = encuestasClientes[i].codigo_agencia.nombre_agencia
				descripcionPregunta = encuestasClientes[i].descripcion_pregunta
				i+=1

			contexto = {
				'encuestasClientes': encuestasClientes,
				'nombreAgencia' : nombreAgencia,
				'tituloEncuesta' : tituloEncuesta,
				'codigoAgencia' : codigo_agencia,
				'descripcionPregunta' : descripcionPregunta,
				'contador' : contador,
			}
				
			return render(
				request, 
				'evaluacionCliente/contestar_encuesta.html', 
				contexto
				)
		
		else:
			mensajeNV = "PreguntaNV"
			contexto = {
				'codigoAgencia' : codigo_agencia,
				'mensajeNV' : mensajeNV,
			}
				
			return render(
				request, 
				'evaluacionCliente/contestar_encuesta.html', 
				contexto
				)


# Obtener el enlace de la encuesta
def consultarEncuestaCliente2(request, codigoAgencia):
	if request.method == 'POST':
		titulo_encuesta = request.POST['titulo_encuesta']
		codigo_agencia = codigoAgencia

		encuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta, visibilidad_pregunta_cliente = 'S')

		enlace = "http://localhost:8000/evaluacionCliente/encuesta/Encuesta22/" + codigo_agencia + "/" + titulo_encuesta

		contexto = {
			'codigoAgencia' : codigo_agencia,
			'enlace' : enlace,
		}
			
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta.html', 
			contexto
			)


# Contestar la encuesta por medio del enlace
def consultarEncuestaCliente22(request, codigoAgencia, tituloEncuesta):
	codigo_agencia = codigoAgencia		
	titulo_encuesta = tituloEncuesta

	encuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta, visibilidad_pregunta_cliente = 'S')

	if len(encuestasClientes) > 0:
		i=0
		contador = i
		while i<1:
			tituloEncuesta = encuestasClientes[i].titulo_encuesta_cliente
			nombreAgencia = encuestasClientes[i].codigo_agencia.nombre_agencia
			descripcionPregunta = encuestasClientes[i].descripcion_pregunta
			i+=1

		contexto = {
			'encuestasClientes': encuestasClientes,
			'nombreAgencia' : nombreAgencia,
			'tituloEncuesta' : tituloEncuesta,
			'codigoAgencia' : codigo_agencia,
			'descripcionPregunta' : descripcionPregunta,
			'contador' : contador,
		}
			
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta.html', 
			contexto
			)
	
	else:
		mensajeNV = "PreguntaNV"
		contexto = {
			'codigoAgencia' : codigo_agencia,
			'mensajeNV' : mensajeNV,
		}
			
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta.html', 
			contexto
			)


# Contestar la Pregunta de esa encuesta
def contestarEncuestaCliente(request, codigoAgencia, tituloEncuesta, descripcionPregunta, contador):
	if request.method == 'POST':
		respuesta = request.POST['respuesta']
		codigo_agencia = codigoAgencia
		titulo_encuesta = tituloEncuesta
		descripcion_pregunta = descripcionPregunta

		encuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta, visibilidad_pregunta_cliente = 'S')
		encuestasClientesResponder = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta, visibilidad_pregunta_cliente = 'S', descripcion_pregunta = descripcion_pregunta)
		
		j=0
		while j < len(encuestasClientesResponder):
			idEncuesta = encuestasClientesResponder[j].id
			j+=1

		responderEncuesta = RespuestaEncuestaCliente(respuesta_cliente = respuesta, encuesta_id = idEncuesta)
		responderEncuesta.save()

		if(contador < (len(encuestasClientes) - 1) ):

			i = contador + 1
			contador2 = i + 1
			contador = i
			while i < (contador2):
				tituloEncuesta = encuestasClientes[i].titulo_encuesta_cliente
				nombreAgencia = encuestasClientes[i].codigo_agencia.nombre_agencia
				descripcionPregunta = encuestasClientes[i].descripcion_pregunta
				i+=1

			if(contador == (len(encuestasClientes) - 1) ):
				contexto = {
					'encuestasClientes': encuestasClientes,
					'nombreAgencia' : nombreAgencia,
					'tituloEncuesta' : tituloEncuesta,
					'codigoAgencia' : codigo_agencia,
					'descripcionPregunta' : descripcionPregunta,
					'contador': contador,
					'fin': "fin",
				}
			else:
				contexto = {
					'encuestasClientes': encuestasClientes,
					'nombreAgencia' : nombreAgencia,
					'tituloEncuesta' : tituloEncuesta,
					'codigoAgencia' : codigo_agencia,
					'descripcionPregunta' : descripcionPregunta,
					'contador': contador,
				}

		else:
			mensaje = "Terminar"

			contexto = {
				'mensaje' : mensaje,
			}
		
			
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta.html', 
			contexto
			)


#----------------------------------------------------------------------------------------------------------------------------------


# LISTAR Agencias para buscar ENCUESTA
def listarRespuestasEncuesta(request):
	agencias = Agencia.objects.all()
	respuestasEncuestaCliente = RespuestaEncuestaCliente.objects.all()

	context = {
		'agenciasCon': agencias,
		'respuestasEncuestaCliente' : respuestasEncuestaCliente,
	}

	return render(
		request,
		'evaluacionCliente/listar_respuestas_clientes.html',
		context
	)


# Mostrar la Encuesta de esa Agencia
def consultarRespuestasAgenciaCliente(request):
	if request.method == 'POST':
		codigo_agencia = request.POST['codigo_agencia']
		
		encuestasAgencia = EncuestaCliente.objects.raw('select id, titulo_encuesta_cliente from proyecto_encuestacliente where codigo_agencia_id = %s group by titulo_encuesta_cliente;', [codigo_agencia])
		nombreAgencia = Agencia.objects.filter(codigo_agencia = codigo_agencia)

		i=0
		while i < len(nombreAgencia):
			codAgencia = nombreAgencia[i].codigo_agencia
			i+=1

		if len(encuestasAgencia) > 0:
			contexto = {
				'encuestasAgencia': encuestasAgencia,
				'nombreAgencia': nombreAgencia,
				'codAgencia': codAgencia,
				'codigo_agencia': codigo_agencia,
			}

		else:
			noHayEncuestas = "NoHay"
		
			contexto = {
				'encuestasAgencia': encuestasAgencia,
				'nombreAgencia': nombreAgencia,
				'codAgencia': codAgencia,
				'codigo_agencia': codigo_agencia,
				'noHayEncuestas': noHayEncuestas,
			}
			
		return render(
			request, 
			'evaluacionCliente/listar_respuestas_clientes.html', 
			contexto
			)


# Mostrar los Resultados de la Encuesta de esa Agencia
def consultarRespuestasEncuestaCliente(request, codigoAgencia):
	if request.method == 'POST':
		titulo_encuesta = request.POST['titulo_encuesta']
		codigo_agencia = codigoAgencia

		#respuestaEncuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta)
		respuestaEncuestasClientes = RespuestaEncuestaCliente.objects.filter(encuesta_id__codigo_agencia = codigo_agencia, encuesta_id__titulo_encuesta_cliente= titulo_encuesta)

		encuestas = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia)
		agencias = Agencia.objects.all()

		if len(respuestaEncuestasClientes) > 0:
			i=0
			while i<1:
				tituloEncuesta = respuestaEncuestasClientes[i].encuesta.titulo_encuesta_cliente
				nombreAgencia = respuestaEncuestasClientes[i].encuesta.codigo_agencia.nombre_agencia
				i+=1


			# Para realizar el conteo
			lista = []
			dic = {}

			i=0
			while i < len(respuestaEncuestasClientes):
				excelente = 0
				regular = 0
				pesimo = 0
				if i == 0:
					pregunta = respuestaEncuestasClientes[i].encuesta.descripcion_pregunta
					
					j=0
					while j < len(respuestaEncuestasClientes):
						if respuestaEncuestasClientes[j].encuesta.descripcion_pregunta == pregunta:
							if respuestaEncuestasClientes[j].respuesta_cliente == 1:
								excelente = excelente + 1
							elif respuestaEncuestasClientes[j].respuesta_cliente == 2:
								regular = regular + 1
							else:
								pesimo = pesimo + 1
						j+=1
					
					dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
					lista.append(dic)
					i+=1
				
				else:
					pregunta = respuestaEncuestasClientes[i].encuesta.descripcion_pregunta
					preguntaAnterior = respuestaEncuestasClientes[(i-1)].encuesta.descripcion_pregunta
					
					if pregunta == preguntaAnterior:
						i+=1
					
					else:
						excelente = 0
						regular = 0
						pesimo = 0
						j=0
						while j < len(respuestaEncuestasClientes):
							if respuestaEncuestasClientes[j].encuesta.descripcion_pregunta == pregunta:
								if respuestaEncuestasClientes[j].respuesta_cliente == 1:
									excelente = excelente + 1
								elif respuestaEncuestasClientes[j].respuesta_cliente == 2:
									regular = regular + 1
								else:
									pesimo = pesimo + 1
							j+=1
						
						dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
						lista.append(dic)
						i+=1

			#Ejemplo de imprimir diccionario en Python
			#for i in lista:
			#	print(i.get('pregunta'))
			
			mylist = json.dumps(lista)

			contexto = {
				'respuestaEncuestasClientes': respuestaEncuestasClientes,
				'agencias': agencias,
				'encuestas': encuestas,
				'nombreAgencia' : nombreAgencia,
				'tituloEncuesta' : tituloEncuesta,
				'codigoAgencia' : codigo_agencia,
				'lista': lista,
				'mylist': mylist,
			}
				
			return render(
				request, 
				'evaluacionCliente/listar_respuestas_clientes.html', 
				contexto
				)
		
		else:
			mensajeVacia = "NoneLista"

			contexto = {
				'agencias': agencias,
				'encuestas': encuestas,
				'mensajeVacia': mensajeVacia,
			}
				
			return render(
				request, 
				'evaluacionCliente/listar_respuestas_clientes.html', 
				contexto
				)

#ROBERTOOOOOOOOOO

def reporteRespuestasEncuestaCliente(request):
	if request.method == 'GET':
		nombreAgencia = request.GET['nombreAgencia']
		tituloEncuesta = request.GET['tituloEncuesta']

		agencia = Agencia.objects.filter(nombre_agencia = nombreAgencia)

		for cod in agencia:
			if cod.nombre_agencia == nombreAgencia:
				codigo_agencia = cod.codigo_agencia

		#respuestaEncuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta)
		respuestaEncuestasClientes = RespuestaEncuestaCliente.objects.filter(encuesta_id__codigo_agencia = codigo_agencia, encuesta_id__titulo_encuesta_cliente= tituloEncuesta)

		encuestas = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia)
		agencias = Agencia.objects.all()

		if len(respuestaEncuestasClientes) > 0:
			i=0
			while i<1:
				tituloEncuesta = respuestaEncuestasClientes[i].encuesta.titulo_encuesta_cliente
				nombreAgencia = respuestaEncuestasClientes[i].encuesta.codigo_agencia.nombre_agencia
				i+=1


			# Para realizar el conteo
			lista = []
			dic = {}

			i=0
			while i < len(respuestaEncuestasClientes):
				excelente = 0
				regular = 0
				pesimo = 0
				if i == 0:
					pregunta = respuestaEncuestasClientes[i].encuesta.descripcion_pregunta
					
					j=0
					while j < len(respuestaEncuestasClientes):
						if respuestaEncuestasClientes[j].encuesta.descripcion_pregunta == pregunta:
							if respuestaEncuestasClientes[j].respuesta_cliente == 1:
								excelente = excelente + 1
							elif respuestaEncuestasClientes[j].respuesta_cliente == 2:
								regular = regular + 1
							else:
								pesimo = pesimo + 1
						j+=1
					
					dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
					lista.append(dic)
					i+=1
				
				else:
					pregunta = respuestaEncuestasClientes[i].encuesta.descripcion_pregunta
					preguntaAnterior = respuestaEncuestasClientes[(i-1)].encuesta.descripcion_pregunta
					
					if pregunta == preguntaAnterior:
						i+=1
					
					else:
						excelente = 0
						regular = 0
						pesimo = 0
						j=0
						while j < len(respuestaEncuestasClientes):
							if respuestaEncuestasClientes[j].encuesta.descripcion_pregunta == pregunta:
								if respuestaEncuestasClientes[j].respuesta_cliente == 1:
									excelente = excelente + 1
								elif respuestaEncuestasClientes[j].respuesta_cliente == 2:
									regular = regular + 1
								else:
									pesimo = pesimo + 1
							j+=1
						
						dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
						lista.append(dic)
						i+=1

		context = {
			'nombreAgencia': nombreAgencia,
			'tituloEncuesta': tituloEncuesta,
			'lista': lista,
			'codigo_agencia': codigo_agencia,
		}

		template = get_template('reportes/reporteRespuestasEncuestaCliente.html')

		html = template.render(context)

		response = HttpResponse(content_type = 'application/pdf')
		response['Content-Disposition'] = 'inline; filename="ReporteRespuestasEncuestaCliente.pdf"'

		pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
	    
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>'+ html + '</pre>')

		return response

def exportarRespuestasEncuestaCliente(request):
	if request.method == 'GET':
		nombreAgencia = request.GET['nombreAgencia']
		tituloEncuesta = request.GET['tituloEncuesta']

		agencia = Agencia.objects.filter(nombre_agencia = nombreAgencia)

		for cod in agencia:
			if cod.nombre_agencia == nombreAgencia:
				codigo_agencia = cod.codigo_agencia

		#respuestaEncuestasClientes = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia, titulo_encuesta_cliente = titulo_encuesta)
		respuestaEncuestasClientes = RespuestaEncuestaCliente.objects.filter(encuesta_id__codigo_agencia = codigo_agencia, encuesta_id__titulo_encuesta_cliente= tituloEncuesta)

		encuestas = EncuestaCliente.objects.filter(codigo_agencia = codigo_agencia)
		agencias = Agencia.objects.all()

		if len(respuestaEncuestasClientes) > 0:
			i=0
			while i<1:
				tituloEncuesta = respuestaEncuestasClientes[i].encuesta.titulo_encuesta_cliente
				nombreAgencia = respuestaEncuestasClientes[i].encuesta.codigo_agencia.nombre_agencia
				i+=1


			# Para realizar el conteo
			lista = []
			dic = {}

			i=0
			while i < len(respuestaEncuestasClientes):
				excelente = 0
				regular = 0
				pesimo = 0
				if i == 0:
					pregunta = respuestaEncuestasClientes[i].encuesta.descripcion_pregunta
					
					j=0
					while j < len(respuestaEncuestasClientes):
						if respuestaEncuestasClientes[j].encuesta.descripcion_pregunta == pregunta:
							if respuestaEncuestasClientes[j].respuesta_cliente == 1:
								excelente = excelente + 1
							elif respuestaEncuestasClientes[j].respuesta_cliente == 2:
								regular = regular + 1
							else:
								pesimo = pesimo + 1
						j+=1
					
					dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
					lista.append(dic)
					i+=1
				
				else:
					pregunta = respuestaEncuestasClientes[i].encuesta.descripcion_pregunta
					preguntaAnterior = respuestaEncuestasClientes[(i-1)].encuesta.descripcion_pregunta
					
					if pregunta == preguntaAnterior:
						i+=1
					
					else:
						excelente = 0
						regular = 0
						pesimo = 0
						j=0
						while j < len(respuestaEncuestasClientes):
							if respuestaEncuestasClientes[j].encuesta.descripcion_pregunta == pregunta:
								if respuestaEncuestasClientes[j].respuesta_cliente == 1:
									excelente = excelente + 1
								elif respuestaEncuestasClientes[j].respuesta_cliente == 2:
									regular = regular + 1
								else:
									pesimo = pesimo + 1
							j+=1
						
						dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
						lista.append(dic)
						i+=1		

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="CSVRespuestasEncuestaCliente.csv"'

		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Estudiantes por Docente') 

		row_num = 0

		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		columns = ['Pregunta', 'Excelente', 'Regular', 'Pesimo']

		for col_num in range(len(columns)):
		    ws.write(row_num, col_num, columns[col_num], font_style) 

			#Ejemplo de imprimir diccionario en Python
			#for i in lista:
			#	print(i.get('pregunta'))

		# Sheet body, remaining rows
		font_style = xlwt.XFStyle()

		for lis in lista:
			row_num += 1
			row = [lis.get('pregunta'), lis.get('excelente'), lis.get('regular'), lis.get('pesimo')]

			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)

		wb.save(response)

		return response	

#----------------------------------------------------------------------------------------------------------------------------------


#Vista para Contestar la Encuesta de Personal
def contestarEncuestaPersonal(request):
	actividades = Actividad.objects.all().order_by('codigo_agencia')

	context = {
		'actividadesCon': actividades,
	}

	return render(
        request,
        'evaluacionCliente/contestar_encuesta_personal.html',
		context
    )


# Mostrar las Agencias
def consultarActividadEncuestaDePersonal(request):
	if request.method == 'POST':
		codigo_actividad = request.POST['codigo_actividad']
		
		encuestasActividad = EncuestaPersonal.objects.raw('select id, titulo_encuesta_personal from proyecto_encuestapersonal where id_actividad_id = %s group by titulo_encuesta_personal;', [codigo_actividad])
		nombreActividad = Actividad.objects.filter(id_actividad = codigo_actividad)
		
		# Procedimiento para validar la Fecha Hasta y asi mostrar la encuesta o no
		fechaHoy = datetime.now().date()
		titulosEncuestas = []
		j=0
		while j < len(encuestasActividad):
			fechaDesde = encuestasActividad[j].fecha_desde_personal
			fechaHasta = encuestasActividad[j].fecha_hasta_personal
			if (fechaHasta == None) or (fechaHasta >= fechaHoy):
				titulosEncuestas.append(encuestasActividad[j].titulo_encuesta_personal)
			j+=1
		
		i=0
		while i < len(nombreActividad):
			codActividad = nombreActividad[i].id_actividad
			i+=1

		if len(encuestasActividad) > 0:
			contexto = {
				'encuestasActividad': encuestasActividad,
				'nombreActividad': nombreActividad,
				'codActividad': codActividad,
				'codigo_actividad': codigo_actividad,
				'titulosEncuestas': titulosEncuestas,
			}

		else:
			noHayEncuestas = "NoHay"
		
			contexto = {
				'encuestasActividad': encuestasActividad,
				'nombreActividad': nombreActividad,
				'codActividad': codActividad,
				'codigo_actividad': codigo_actividad,
				'noHayEncuestas': noHayEncuestas,
				'titulosEncuestas': titulosEncuestas,
			}
			
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta_personal.html', 
			contexto
			)
		

# Mostrar la Encuesta de esa Agencia
def consultarEncuestaDePersonal(request, idActividad):
	if request.method == 'POST':
		titulo_encuesta = request.POST['titulo_encuesta']
		codigo_actividad = idActividad

		encuestasPersonal = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad, titulo_encuesta_personal = titulo_encuesta, visibilidad_pregunta_personal = 'S')
		
		encuestas = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad)
		actividades = Actividad.objects.all()

		if len(encuestasPersonal) > 0:
			i=0
			contador = i
			while i<1:
				tituloEncuesta = encuestasPersonal[i].titulo_encuesta_personal
				nombreAgencia = encuestasPersonal[i].id_actividad.codigo_agencia.nombre_agencia
				nombreActividad = encuestasPersonal[i].id_actividad.nombre_actividad
				descripcionPregunta = encuestasPersonal[i].descripcion_pregunta
				i+=1

			contexto = {
				'encuestasPersonal': encuestasPersonal,
				'actividades': actividades,
				'encuestas': encuestas,
				'nombreAgencia' : nombreAgencia,
				'nombreActividad' : nombreActividad,
				'tituloEncuesta' : tituloEncuesta,
				'codigoActividad' : codigo_actividad,
				'descripcionPregunta' : descripcionPregunta,
				'contador' : contador,
			}
				
			return render(
				request, 
				'evaluacionCliente/contestar_encuesta_personal.html', 
				contexto
				)

		else:
			mensajeNV = "PreguntaNV"
			contexto = {
				'actividades': actividades,
				'encuestas': encuestas,
				'codigoActividad' : codigo_actividad,
				'mensajeNV' : mensajeNV,
			}
				
			return render(
				request, 
				'evaluacionCliente/contestar_encuesta_personal.html', 
				contexto
				)


# Obtener el enlace de la encuesta
def consultarEncuestaDePersonal2(request, idActividad):
	if request.method == 'POST':
		titulo_encuesta = request.POST['titulo_encuesta']
		codigo_actividad = idActividad

		encuestasPersonal = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad, titulo_encuesta_personal = titulo_encuesta, visibilidad_pregunta_personal = 'S')
		
		encuestas = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad)
		actividades = Actividad.objects.all()

		enlace = "http://localhost:8000/evaluacionCliente/encuestaPersonal/Encuesta22/" + codigo_actividad + "/" + titulo_encuesta
		 
		contexto = {
			'actividades': actividades,
			'encuestas': encuestas,
			'codigoActividad' : codigo_actividad,
			'enlace' : enlace,
		}
			
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta_personal.html', 
			contexto
			)


# Contestar la encuesta por medio del enlace
def consultarEncuestaDePersonal22(request, idActividad, tituloEncuestaPersonal):
	codigo_actividad = idActividad
	titulo_encuesta = tituloEncuestaPersonal

	encuestasPersonal = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad, titulo_encuesta_personal = titulo_encuesta, visibilidad_pregunta_personal = 'S')
	
	encuestas = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad)
	actividades = Actividad.objects.all()

	if len(encuestasPersonal) > 0:
		i=0
		contador = i
		while i<1:
			tituloEncuesta = encuestasPersonal[i].titulo_encuesta_personal
			nombreAgencia = encuestasPersonal[i].id_actividad.codigo_agencia.nombre_agencia
			nombreActividad = encuestasPersonal[i].id_actividad.nombre_actividad
			descripcionPregunta = encuestasPersonal[i].descripcion_pregunta
			i+=1

		contexto = {
			'encuestasPersonal': encuestasPersonal,
			'actividades': actividades,
			'encuestas': encuestas,
			'nombreAgencia' : nombreAgencia,
			'nombreActividad' : nombreActividad,
			'tituloEncuesta' : tituloEncuesta,
			'codigoActividad' : codigo_actividad,
			'descripcionPregunta' : descripcionPregunta,
			'contador' : contador,
		}
			
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta_personal.html', 
			contexto
			)

	else:
		mensajeNV = "PreguntaNV"
		contexto = {
			'actividades': actividades,
			'encuestas': encuestas,
			'codigoActividad' : codigo_actividad,
			'mensajeNV' : mensajeNV,
		}
			
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta_personal.html', 
			contexto
			)


# Contestar la Pregunta de esa encuesta
def contestarEncuestaDePersonal(request, idActividad, tituloEncuesta, descripcionPregunta, contador):
	if request.method == 'POST':
		respuesta = request.POST['respuesta']
		codigo_actividad = idActividad
		titulo_encuesta = tituloEncuesta
		descripcion_pregunta = descripcionPregunta

		encuestasPersonal = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad, titulo_encuesta_personal = titulo_encuesta, visibilidad_pregunta_personal = 'S')
		encuestasPersonalResponder = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad, titulo_encuesta_personal = titulo_encuesta, visibilidad_pregunta_personal = 'S', descripcion_pregunta = descripcion_pregunta)
		
		j=0
		while j < len(encuestasPersonalResponder):
			idEncuesta = encuestasPersonalResponder[j].id
			j+=1

		responderEncuesta = RespuestaEncuestaPersonal(respuesta_personal = respuesta, encuesta_id = idEncuesta)
		responderEncuesta.save()

		if(contador < (len(encuestasPersonal) - 1) ):

			i = contador + 1
			contador2 = i + 1
			contador = i
			while i < (contador2):
				tituloEncuesta = encuestasPersonal[i].titulo_encuesta_personal
				nombreActividad = encuestasPersonal[i].id_actividad.nombre_actividad
				descripcionPregunta = encuestasPersonal[i].descripcion_pregunta
				i+=1

			if(contador == (len(encuestasPersonal) - 1) ):
				contexto = {
					'encuestasPersonal': encuestasPersonal,
					'nombreActividad' : nombreActividad,
					'tituloEncuesta' : tituloEncuesta,
					'codigoActividad' : codigo_actividad,
					'descripcionPregunta' : descripcionPregunta,
					'contador': contador,
					'fin': "fin",
				}
			
			else:
				contexto = {
					'encuestasPersonal': encuestasPersonal,
					'nombreActividad' : nombreActividad,
					'tituloEncuesta' : tituloEncuesta,
					'codigoActividad' : codigo_actividad,
					'descripcionPregunta' : descripcionPregunta,
					'contador': contador,
				}

		else:
			mensaje = "Terminar"

			contexto = {
				'mensaje' : mensaje,
			}
			
		return render(
			request, 
			'evaluacionCliente/contestar_encuesta_personal.html', 
			contexto
			)


#----------------------------------------------------------------------------------------------------------------------------------


# LISTAR Agencias para buscar ENCUESTA PERSONAL
def listarRespuestasEncuestaPersonal(request):
	actividades = Actividad.objects.all().order_by('codigo_agencia')
	respuestasEncuestaPersonal = RespuestaEncuestaPersonal.objects.all()

	context = {
		'actividadesCon': actividades,
		'respuestasEncuestaPersonal' : respuestasEncuestaPersonal,
	}

	return render(
		request,
		'evaluacionCliente/listar_respuestas_personal.html',
		context
	)


# Mostrar la Encuesta de esa Agencia
def consultarRespuestasActividadPersonal(request):
	if request.method == 'POST':
		codigo_actividad = request.POST['codigo_actividad']
		
		encuestasActividad = EncuestaPersonal.objects.raw('select id, titulo_encuesta_personal from proyecto_encuestapersonal where id_actividad_id = %s group by titulo_encuesta_personal;', [codigo_actividad])
		nombreActividad = Actividad.objects.filter(id_actividad = codigo_actividad)
		
		i=0
		while i < len(nombreActividad):
			codActividad = nombreActividad[i].id_actividad
			i+=1

		if len(encuestasActividad) > 0:
			contexto = {
				'encuestasActividad': encuestasActividad,
				'nombreActividad': nombreActividad,
				'codActividad': codActividad,
				'codigo_actividad': codigo_actividad,
			}

		else:
			noHayEncuestas = "NoHay"
		
			contexto = {
				'encuestasActividad': encuestasActividad,
				'nombreActividad': nombreActividad,
				'codActividad': codActividad,
				'codigo_actividad': codigo_actividad,
				'noHayEncuestas': noHayEncuestas,
			}
			
		return render(
			request, 
			'evaluacionCliente/listar_respuestas_personal.html', 
			contexto
			)


# Mostrar los Resultados de la Encuesta de esa Agencia en PDF
def consultarRespuestasEncuestaPersonal(request, idActividad):
	if request.method == 'POST':
		titulo_encuesta = request.POST['titulo_encuesta']
		codigo_actividad = idActividad

		respuestaEncuestasPersonal = RespuestaEncuestaPersonal.objects.filter(encuesta_id__id_actividad = codigo_actividad, encuesta_id__titulo_encuesta_personal = titulo_encuesta)

		encuestas = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad)
		actividades = Actividad.objects.all()

		if len(respuestaEncuestasPersonal) > 0:
			i=0
			while i<1:
				tituloEncuesta = respuestaEncuestasPersonal[i].encuesta.titulo_encuesta_personal
				nombreActividad = respuestaEncuestasPersonal[i].encuesta.id_actividad.nombre_actividad
				i+=1


			# Para realizar el conteo
			lista = []
			dic = {}

			i=0
			while i < len(respuestaEncuestasPersonal):
				excelente = 0
				regular = 0
				pesimo = 0
				if i == 0:
					pregunta = respuestaEncuestasPersonal[i].encuesta.descripcion_pregunta
					
					j=0
					while j < len(respuestaEncuestasPersonal):
						if respuestaEncuestasPersonal[j].encuesta.descripcion_pregunta == pregunta:
							if respuestaEncuestasPersonal[j].respuesta_personal == 1:
								excelente = excelente + 1
							elif respuestaEncuestasPersonal[j].respuesta_personal == 2:
								regular = regular + 1
							else:
								pesimo = pesimo + 1
						j+=1
					
					dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
					lista.append(dic)
					i+=1
				
				else:
					pregunta = respuestaEncuestasPersonal[i].encuesta.descripcion_pregunta
					preguntaAnterior = respuestaEncuestasPersonal[(i-1)].encuesta.descripcion_pregunta
					
					if pregunta == preguntaAnterior:
						i+=1
					
					else:
						excelente = 0
						regular = 0
						pesimo = 0
						j=0
						while j < len(respuestaEncuestasPersonal):
							if respuestaEncuestasPersonal[j].encuesta.descripcion_pregunta == pregunta:
								if respuestaEncuestasPersonal[j].respuesta_personal == 1:
									excelente = excelente + 1
								elif respuestaEncuestasPersonal[j].respuesta_personal == 2:
									regular = regular + 1
								else:
									pesimo = pesimo + 1
							j+=1
						
						dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
						lista.append(dic)
						i+=1

			#Ejemplo de imprimir diccionario en Python
			#for i in lista:
			#	print(i.get('pregunta'))

			mylist = json.dumps(lista)
			
			contexto = {
				'respuestaEncuestasPersonal': respuestaEncuestasPersonal,
				'actividades': actividades,
				'encuestas': encuestas,
				'nombreActividad' : nombreActividad,
				'tituloEncuesta' : tituloEncuesta,
				'codigoActividad' : codigo_actividad,
				'lista': lista,
				'mylist': mylist,
			}
				
			return render(
				request, 
				'evaluacionCliente/listar_respuestas_personal.html', 
				contexto
				)
		
		else:
			mensajeVacia = "NoneLista"

			contexto = {
				'actividades': actividades,
				'encuestas': encuestas,
				'mensajeVacia': mensajeVacia,
			}
				
			return render(
				request, 
				'evaluacionCliente/listar_respuestas_personal.html', 
				contexto
				)

#ROBERTOOOOOOOOOO

def reporteRespuestasEncuestaPersonal(request):
	if request.method == 'GET':
		nombreAc = request.GET['nombreActividad']
		titulo_encuesta = request.GET['tituloEncuesta']

		actividad = Actividad.objects.filter(nombre_actividad = nombreAc)

		for ac in actividad:
			if ac.nombre_actividad == nombreAc:
				codigo_actividad = ac.id_actividad

		respuestaEncuestasPersonal = RespuestaEncuestaPersonal.objects.filter(encuesta_id__id_actividad = codigo_actividad, encuesta_id__titulo_encuesta_personal = titulo_encuesta)

		encuestas = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad)
		actividades = Actividad.objects.all()

		if len(respuestaEncuestasPersonal) > 0:
			i=0
			while i<1:
				tituloEncuesta = respuestaEncuestasPersonal[i].encuesta.titulo_encuesta_personal
				nombreActividad = respuestaEncuestasPersonal[i].encuesta.id_actividad.nombre_actividad
				i+=1


			# Para realizar el conteo
			lista = []
			dic = {}

			i=0
			while i < len(respuestaEncuestasPersonal):
				excelente = 0
				regular = 0
				pesimo = 0
				if i == 0:
					pregunta = respuestaEncuestasPersonal[i].encuesta.descripcion_pregunta
					
					j=0
					while j < len(respuestaEncuestasPersonal):
						if respuestaEncuestasPersonal[j].encuesta.descripcion_pregunta == pregunta:
							if respuestaEncuestasPersonal[j].respuesta_personal == 1:
								excelente = excelente + 1
							elif respuestaEncuestasPersonal[j].respuesta_personal == 2:
								regular = regular + 1
							else:
								pesimo = pesimo + 1
						j+=1
					
					dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
					lista.append(dic)
					i+=1
				
				else:
					pregunta = respuestaEncuestasPersonal[i].encuesta.descripcion_pregunta
					preguntaAnterior = respuestaEncuestasPersonal[(i-1)].encuesta.descripcion_pregunta
					
					if pregunta == preguntaAnterior:
						i+=1
					
					else:
						excelente = 0
						regular = 0
						pesimo = 0
						j=0
						while j < len(respuestaEncuestasPersonal):
							if respuestaEncuestasPersonal[j].encuesta.descripcion_pregunta == pregunta:
								if respuestaEncuestasPersonal[j].respuesta_personal == 1:
									excelente = excelente + 1
								elif respuestaEncuestasPersonal[j].respuesta_personal == 2:
									regular = regular + 1
								else:
									pesimo = pesimo + 1
							j+=1
						
						dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
						lista.append(dic)
						i+=1

		context = {
			'respuestaEncuestasPersonal': respuestaEncuestasPersonal,
			'nombreAc': nombreAc,
			'tituloEncuesta': tituloEncuesta,
			'lista': lista,
		}

		template = get_template('reportes/reporteRespuestasEncuestaPersonal.html')

		html = template.render(context)

		response = HttpResponse(content_type = 'application/pdf')
		response['Content-Disposition'] = 'inline; filename="ReporteRespuestasEncuestaPersonal.pdf"'

		pisa_status = pisa.CreatePDF(html, dest = response, link_callback=link_callback)
	    
		if pisa_status.err:
			return HttpResponse('We had some errors <pre>'+ html + '</pre>')

		return response

def exportarRespuestasEncuestaPersonal(request):
	if request.method == 'GET':
		nombreAc = request.GET['nombreActividad']
		titulo_encuesta = request.GET['tituloEncuesta']

		actividad = Actividad.objects.filter(nombre_actividad = nombreAc)

		for ac in actividad:
			if ac.nombre_actividad == nombreAc:
				codigo_actividad = ac.id_actividad

		respuestaEncuestasPersonal = RespuestaEncuestaPersonal.objects.filter(encuesta_id__id_actividad = codigo_actividad, encuesta_id__titulo_encuesta_personal = titulo_encuesta)

		encuestas = EncuestaPersonal.objects.filter(id_actividad = codigo_actividad)
		actividades = Actividad.objects.all()

		if len(respuestaEncuestasPersonal) > 0:
			i=0
			while i<1:
				tituloEncuesta = respuestaEncuestasPersonal[i].encuesta.titulo_encuesta_personal
				nombreActividad = respuestaEncuestasPersonal[i].encuesta.id_actividad.nombre_actividad
				i+=1


			# Para realizar el conteo
			lista = []
			dic = {}

			i=0
			while i < len(respuestaEncuestasPersonal):
				excelente = 0
				regular = 0
				pesimo = 0
				if i == 0:
					pregunta = respuestaEncuestasPersonal[i].encuesta.descripcion_pregunta
					
					j=0
					while j < len(respuestaEncuestasPersonal):
						if respuestaEncuestasPersonal[j].encuesta.descripcion_pregunta == pregunta:
							if respuestaEncuestasPersonal[j].respuesta_personal == 1:
								excelente = excelente + 1
							elif respuestaEncuestasPersonal[j].respuesta_personal == 2:
								regular = regular + 1
							else:
								pesimo = pesimo + 1
						j+=1
					
					dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
					lista.append(dic)
					i+=1
				
				else:
					pregunta = respuestaEncuestasPersonal[i].encuesta.descripcion_pregunta
					preguntaAnterior = respuestaEncuestasPersonal[(i-1)].encuesta.descripcion_pregunta
					
					if pregunta == preguntaAnterior:
						i+=1
					
					else:
						excelente = 0
						regular = 0
						pesimo = 0
						j=0
						while j < len(respuestaEncuestasPersonal):
							if respuestaEncuestasPersonal[j].encuesta.descripcion_pregunta == pregunta:
								if respuestaEncuestasPersonal[j].respuesta_personal == 1:
									excelente = excelente + 1
								elif respuestaEncuestasPersonal[j].respuesta_personal == 2:
									regular = regular + 1
								else:
									pesimo = pesimo + 1
							j+=1
						
						dic = {'pregunta': pregunta, 'excelente': excelente, 'regular': regular, 'pesimo': pesimo}
						lista.append(dic)
						i+=1
	    
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="CSVRespuestasEncuestaPersonal.csv"'

		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Estudiantes por Docente') 

		row_num = 0

		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		columns = ['Pregunta', 'Excelente', 'Regular', 'Pesimo']

		for col_num in range(len(columns)):
		    ws.write(row_num, col_num, columns[col_num], font_style) 

			#Ejemplo de imprimir diccionario en Python
			#for i in lista:
			#	print(i.get('pregunta'))

		# Sheet body, remaining rows
		font_style = xlwt.XFStyle()

		for lis in lista:
			row_num += 1
			row = [lis.get('pregunta'), lis.get('excelente'), lis.get('regular'), lis.get('pesimo')]

			for col_num in range(len(row)):
				ws.write(row_num, col_num, row[col_num], font_style)

		wb.save(response)

		return response		
