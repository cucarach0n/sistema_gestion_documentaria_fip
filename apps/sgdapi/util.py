#from multiprocessing import context
#from re import template
#from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(data):
    context = {'email':data['email'],'domain':data['domain']}
    template = get_template('correo.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'Email de validacion',
        settings.EMAIL_HOST_USER,
        [data['email']]
    )

    email.attach_alternative(content,'text/html')
    email.send()
    return content