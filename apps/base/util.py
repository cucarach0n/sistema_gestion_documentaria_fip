from datetime import datetime
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from decouple import config
from os import remove
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from pdf2image import convert_from_path
from apps.folder.models import FolderInFolder
from django.utils.crypto import get_random_string
pytesseract.pytesseract.tesseract_cmd = config('TESSERACT_CMD_PATH')#r'C:\Program Files\Tesseract-OCR\tesseract'
#config('TESSERACT_CMD_PATH')
def send_email(data):
    context = {'email':data['email'],'domain':data['domain']}
    #template = get_template(settings.TEMPLATE_DIRS[0].replace("\\","/")[:64] +'/templates/correo.html')#64 windows / 66 linux
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
def obtenerRuta(padreId,ruta,logico):
        #si el padre es null
        folderinfolder = FolderInFolder.objects.filter(child_folder_id = padreId).select_related('child_folder').first()
        if folderinfolder:
            if logico:
                ruta.append(folderinfolder.parent_folder.nombre) 
            else:
                ruta.append(folderinfolder.parent_folder.slug) 
            obtenerRuta(folderinfolder.parent_folder_id,ruta,logico )
        return ' > '.join(ruta[::-1])


def setHistory(model,razon,user):
    history = model.historical.filter(id = model.id).first()
    history.history_user_id = user
    history.history_change_reason = razon
    history.save()

'''history = fHijo.historical.create(id=folderPadre.id,history_date = datetime.today()
                                                    ,history_change_reason = "Se agrego la carpeta " + fHijo.nombre.replace(" ","_") 
                                                    ,history_type = "+", history_user_id = self.userFull.id )
history.save()'''
def createHistory(model,id,reason,type,userId):
    history = model.historical.create(id=id,history_date = datetime.today(),history_change_reason=reason,history_type=type,history_user_id=userId)
    history.save()

class DocumentoOCR():
    PDF_file = None
    def __init__(self,ruta):
        self.PDF_file = ruta
    def obtenerTexto(self):
        doc = self.PDF_file
        print('Documento : ' + doc)
        absURl = settings.MEDIA_ROOT +'files'  + doc
        print('obteniendo texto de ' + absURl)
        pages = convert_from_path(
            absURl,
            thread_count=8,
            poppler_path=config('POPPLER_PATH_WINDOWS')
        )

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
    
        for i in range(1, filelimit + 1):
            #filename = "page_"+str(i)+".jpg"
            filename = imagenesRutas[i -1]
            # open image
            im = Image.open(settings.MEDIA_ROOT+'test/'+filename)

            # preprocessing
            im = im.convert('L')                             # grayscale
            im = im.filter(ImageFilter.MedianFilter())       # a little blur
            im = im.point(lambda x: 0 if x < 140 else 255)   # threshold (binarize)

            text = str(((pytesseract.image_to_string(im))))
            remove(settings.MEDIA_ROOT+'test/'+filename)
            text = text.replace('-\n', '')   
            percent =  (i*100)/filelimit
            print(str(round(percent,2)) + " %")
            textGenerado += text
        
        print('devolviendo texto')
        return textGenerado
        #return 'test'