#from multiprocessing import context
#from re import template
#from django.shortcuts import render
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from decouple import config

from PIL import Image
import pytesseract
from pdf2image import convert_from_path
pytesseract.pytesseract.tesseract_cmd = config('TESSERACT_CMD_PATH')#r'C:\Program Files\Tesseract-OCR\tesseract'
#config('TESSERACT_CMD_PATH')
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

class DocumentoOCR():
    PDF_file = None
    def __init__(self,ruta):
        self.PDF_file = ruta
    #config('POPPLER_PATH_WINDOWS')
    def obtenerTexto(self):
        doc = self.PDF_file[6:]
        absURl = settings.MEDIA_ROOT.replace("\\","/")  + doc
        print('obteniendo texto de ' + absURl.replace("/","\\"))
        pages = convert_from_path(absURl.replace("/","\\"), 500, poppler_path=config('POPPLER_PATH_WINDOWS'))#r'C:\Program Files\poppler-0.68.0\bin'
        image_counter = 1
        for page in pages:
            filename = "page_"+str(image_counter)+".jpg"
            page.save(filename, 'JPEG')
            image_counter = image_counter + 1
        filelimit = image_counter-1
        textGenerado = ""
        for i in range(1, filelimit + 1):
            filename = "page_"+str(i)+".jpg"
            text = str(((pytesseract.image_to_string(Image.open(filename)))))
            text = text.replace('-\n', '')    
            textGenerado += text
        return textGenerado
