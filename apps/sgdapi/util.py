#from multiprocessing import context
#from re import template
#from django.shortcuts import render
from pathlib import Path
from platform import python_branch
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import tempfile
from decouple import config
from os import remove
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

from django.utils.crypto import get_random_string
pytesseract.pytesseract.tesseract_cmd = config('TESSERACT_CMD_PATH')#r'C:\Program Files\Tesseract-OCR\tesseract'
#config('TESSERACT_CMD_PATH')
def send_email(data):
    context = {'email':data['email'],'domain':data['domain']}
    template = get_template(settings.TEMPLATE_DIRS[0].replace("\\","/")[:64] +'/templates/correo.html')#64 windows / 66 linux
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
        doc = self.PDF_file
        print('Documento : ' + doc)
        absURl = settings.MEDIA_ROOT +'files'  + doc
        print('obteniendo texto de ' + absURl)
        
        #with tempfile.TemporaryDirectory() as path:
        pages = convert_from_path(
            absURl,
            #output_folder=settings.MEDIA_ROOT + "test/",
            thread_count=8,
            poppler_path=config('POPPLER_PATH_WINDOWS')
        )

        #print(path)
        image_counter = 1
        imagenesRutas = []
        for page in pages:
            filename = get_random_string(length=40) + ".jpg"
            imagenesRutas.append(filename)
            page.save(settings.MEDIA_ROOT+'test/'+filename, 'JPEG')
            image_counter = image_counter + 1
        del pages
        filelimit = image_counter-1
        textGenerado = ""
        '''
        pages = convert_from_path(absURl, 500, poppler_path=config('POPPLER_PATH_WINDOWS'))#r'C:\Program Files\poppler-0.68.0\bin'
        
        image_counter = 1
        for page in pages:
            filename = "page_"+str(image_counter)+".jpg"
            print(filename)
            page.save(settings.MEDIA_ROOT.replace("\\","/")+'test/'+filename, 'JPEG')
            image_counter = image_counter + 1

        filelimit = image_counter-1
        textGenerado = ""
        '''
        
        for i in range(1, filelimit + 1):
            #filename = "page_"+str(i)+".jpg"
            filename = imagenesRutas[i -1]
            text = str(((pytesseract.image_to_string(Image.open(settings.MEDIA_ROOT+'test/'+filename)))))
            remove(settings.MEDIA_ROOT+'test/'+filename)
            text = text.replace('-\n', '')   
            percent =  (i*100)/filelimit
            print(str(round(percent,2)) + " %")
            textGenerado += text
        
        print('devolviendo texto')
        return textGenerado
        #return 'test'