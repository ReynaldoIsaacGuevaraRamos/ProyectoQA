from django.test import TestCase

# Create your tests here.
#Enviar correo de Invitacion 
def enviarEmail(self):
	try:
		# Establecemos conexion con el servidor smtp de gmail
		mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
		print(mailServer.ehlo())
		mailServer.starttls()
		print(mailServer.ehlo())
		mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
		print('...Conectado')

		# Construimos el mensaje simple
		mensaje = MIMEText("""Este es el mensaje
		de las narices""")
		mensaje['From']= settings.EMAIL_HOST_USER
		mensaje['To']="pr17017@ues.edu.sv"
		mensaje['Subject']="Tienes un correo"

		# Envio del mensaje
		mailServer.sendmail(settings.EMAIL_HOST_USER,
		                "pr17017@ues.edu.sv",
		                mensaje.as_string())

		print('Correo enviado correctamente')		

	except Exception as e:
		print(e)