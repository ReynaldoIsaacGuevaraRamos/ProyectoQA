from django import forms
from .models import *
import re

#----------------------------------------------------------------------------------------------------------------------------------


class DepartamentoForm(forms.ModelForm):
	class Meta:
		model = Departamento
		fields = {'codigo_departamento', 'nombre_departamento'}

	codigo_departamento = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '([A-Za-z0-9]+)', 'title': 'No se permiten espacios, solo numeros y letras'}))
	nombre_departamento = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))   

	def __init__(self, *args, **kwargs):
		super(DepartamentoForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			self.fields['codigo_departamento'].widget.attrs['readonly'] = True

	def clean_codigo_departamento(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			return instance.codigo_departamento
		else:
			return self.cleaned_data['codigo_departamento']


#----------------------------------------------------------------------------------------------------------------------------------


class ComiteForm(forms.ModelForm):
	class Meta:
		model = Comite
		fields = {'nombre_comite', 'descripcion_comite'}

	nombre_comite = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	descripcion_comite = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 


#----------------------------------------------------------------------------------------------------------------------------------


class AgenciaForm(forms.ModelForm):
	class Meta:
		model = Agencia
		fields = {'codigo_agencia', 'nombre_agencia', 'direccion_agencia'}		

	codigo_agencia = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'pattern': '([A-Za-z0-9]+)', 'title': 'No se permiten espacios, solo numeros y letras'}))
	nombre_agencia = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))   
	direccion_agencia = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))   

	def __init__(self, *args, **kwargs):
		super(AgenciaForm, self).__init__(*args, **kwargs)
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			self.fields['codigo_agencia'].widget.attrs['readonly'] = True

	def clean_codigo_agencia(self):
		instance = getattr(self, 'instance', None)
		if instance and instance.pk:
			return instance.codigo_agencia
		else:
			return self.cleaned_data['codigo_agencia']  


#----------------------------------------------------------------------------------------------------------------------------------


class ActividadForm(forms.ModelForm):
	class Meta:
		model = Actividad
		fields = {'nombre_actividad', 'descripcion_actividad', 'fecha_realizacion', 'codigo_agencia', 'codigo_departamento', 'id_comite'}

	nombre_actividad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	descripcion_actividad = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))   
	fecha_realizacion = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'Fecha de Inicio', 'autocomplete': 'off', 'type':'date', 'min':'1940-01-01', 'class': 'form-control'})) 
	codigo_agencia= forms.ModelChoiceField(queryset=Agencia.objects.all(), empty_label="Seleccione una Agencia de la lista", widget=forms.Select(attrs={'class': 'form-control'}))
	codigo_departamento= forms.ModelChoiceField(queryset=Departamento.objects.all(), empty_label="Seleccione un Departamento de la lista", widget=forms.Select(attrs={'class': 'form-control'}))
	id_comite= forms.ModelChoiceField(queryset=Comite.objects.all(), empty_label="Seleccione un Comite de la lista", widget=forms.Select(attrs={'class': 'form-control'}))

	def __init__(self, *args, **kwargs):
	        super(ActividadForm, self).__init__(*args, **kwargs)
	        self.fields['codigo_agencia'].queryset = Agencia.objects.all()
	        self.fields['codigo_agencia'].label_from_instance = lambda obj: "%s" % (obj.nombre_agencia)
        	self.fields['codigo_agencia'].widget.attrs['class'] = 'form-control'
        	self.fields['codigo_agencia'].widget.attrs['placeholder'] = 'Seleccione una Agencia de la lista'

#----------------------------------------------------------------------------------------------------------------------------------



class EmpleadoForm(forms.ModelForm):	
	class Meta:
		model=Empleado
		fields=('codigo_agencia', 'codigo_departamento', 'id_comite', 'email', 'nombres', 'apellidos')		

		widgets ={
			'email': forms.EmailInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese su Correo Electronico',
				}
			),
			'nombres': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese sus Nombres',
				}
			),
			'apellidos': forms.TextInput(
				attrs={
					'class': 'form-control',
					'placeholder': 'Ingrese sus Apellidos',
				}
			),
		
		}

	codigo_agencia= forms.ModelChoiceField(queryset=Agencia.objects.all(), empty_label="Seleccione una Agencia de la lista", widget=forms.Select(attrs={'class': 'form-control'}))
	codigo_departamento= forms.ModelChoiceField(queryset=Departamento.objects.all(), empty_label="Seleccione un Departamento de la lista",widget=forms.Select(attrs={'class': 'form-control'}))
	id_comite= forms.ModelChoiceField(queryset=Comite.objects.all(), empty_label="Seleccione un Comite de la lista",widget=forms.Select(attrs={'class': 'form-control'}))


	def __init__(self, *args, **kwargs):
	        super(EmpleadoForm, self).__init__(*args, **kwargs)
	        self.fields['codigo_agencia'].queryset = Agencia.objects.all()
	        self.fields['codigo_agencia'].label_from_instance = lambda obj: "%s" % (obj.nombre_agencia)
        	self.fields['codigo_agencia'].widget.attrs['class'] = 'form-control'
        	self.fields['codigo_agencia'].widget.attrs['placeholder'] = 'Seleccione una Agencia de la lista'


	def clean_nombres(self):
		nombres=self.cleaned_data.get('nombres')
		regex = re.compile('^[A-Za-zÁÉÍÓÚáéíóúñÑüÜ ]+$')

		if not regex.match(nombres):
			raise forms.ValidationError('Los nombres no deben contener, caracteres especiales, ni números')
		if not 2 <= len(nombres) <= 100:
			raise forms.ValidationError('Los nombres deben de contener mas caracteres')
		return nombres

	def clean_apellidos(self):
		apellidos=self.cleaned_data.get('apellidos')
		regex = re.compile('^[A-Za-zÁÉÍÓÚáéíóúñÑüÜ ]+$')

		if not regex.match(apellidos):
			raise forms.ValidationError('Los apellidos no deben contener, caracteres especiales, ni números')		
		if not 2 <= len(apellidos) <= 100:
			raise forms.ValidationError('Los apellidos deben de contener mas caracteres')
		return apellidos