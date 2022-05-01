from datetime import datetime
import os
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from apps.share.models import FolderShare
from apps.file.models import File, FileInFolder
from decouple import config
from os import remove
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from pdf2image import convert_from_path
from apps.folder.models import Folder, FolderInFolder
from django.utils.crypto import get_random_string
import platform
from django.db.models import Q

import unicodedata
from django.core.files.storage import FileSystemStorage
from django.db import transaction
os.environ['OMP_THREAD_LIMIT'] = '1'
sistema = platform.system()
if(sistema == "Windows"):
    pytesseract.pytesseract.tesseract_cmd = config('TESSERACT_CMD_PATH')#r'C:\Program Files\Tesseract-OCR\tesseract'

#config('TESSERACT_CMD_PATH')



class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """
    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)

def send_email(data):
    context = {'email':data['email'],'domain':data['domain'],'usuario':data['usuario'],'password':data['password']}
    #template = get_template(settings.TEMPLATE_DIRS[0].replace("\\","/")[:64] +'/templates/correo.html')#64 windows / 66 linux
    template = get_template('correo.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Bienvenido al Sistema de Gestion Documentaria FIP',
        'Credenciales de acceso para '+ data['usuario'].name +" " + data['usuario'].last_name,
        "Registro de cuenta FIP <"+settings.EMAIL_HOST_USER+">",
        [data['email']]
    )

    email.attach_alternative(content,'text/html')
    email.send()
    return content
def obtenerRuta(padreId,ruta,logico,privado = False,getPrivate = False,userId = None):
        
        #si el padre es null
        folderinfolder = FolderInFolder.objects.filter(child_folder_id = padreId).select_related('child_folder').first()
        if folderinfolder:
            #print(folderinfolder.parent_folder.scope)
            if getPrivate:
                if not privado:
                    if folderinfolder.parent_folder.scope == False:
                        if folderinfolder.parent_folder.user_id == userId:
                            privado = False
                        else:
                            privado = True
            if logico:
                ruta.append(folderinfolder.parent_folder.nombre) 
            else:
                ruta.append(folderinfolder.parent_folder.slug) 
            obtenerRuta(folderinfolder.parent_folder_id,ruta,logico,privado,getPrivate)
        #print(privado)
        if getPrivate:
            return privado
        else:
            return ' > '.join(ruta[::-1])
def validarCompartido(foldeSlug,compartido = False,userId = None):
    folderinfolder = FolderInFolder.objects.filter(child_folder__slug = foldeSlug).select_related('child_folder').first()
    if folderinfolder:
        
        if not compartido:
            '''folderShareResultSame = FolderShare.objects.filter(folder_id = folderinfolder.child_folder.id).select_related('folder').first()
            if folderShareResultSame:
                if folderShareResultSame.estado == True and folderShareResultSame.userTo_id == userId:
                    return True
            folderShareResult = FolderShare.objects.filter(folder_id = folderinfolder.parent_folder.id).select_related('folder').first()
            if folderShareResult:
                print('folder share es ' + folderShareResult.folder.nombre + ', estado '+ str(folderShareResult.estado))
                if folderShareResult.estado == True:
                    if folderShareResult.userTo_id == userId:
                        compartido = True
                    else:
                        compartido = False'''
            folderShareResult = FolderShare.objects.filter(Q(folder_id = folderinfolder.parent_folder.id)
                                                        |Q(folder_id = folderinfolder.child_folder.id)
                                                        ,estado =True,userTo_id = userId).select_related('folder').distinct().first()
            if folderShareResult:
                compartido = True
            else:
                compartido = False
        validarCompartido(folderinfolder.parent_folder.slug,compartido,userId)
        
    return compartido
@transaction.atomic
def setPublicHijos(foldeSlug):
    folders = Folder.objects.filter(carpeta_hija__parent_folder__slug = foldeSlug)
    for folder in folders:
        print(folder)
        folder.scope = True
        folder.save()
        File.objects.filter(fileinfolder__parent_folder_id = folder.id).update(scope = True)
        setPublicHijos(folder.slug)
@transaction.atomic
def setEliminarHijos(foldeSlug,eliminar = True):
    folders = Folder.objects.filter(carpeta_hija__parent_folder__slug = foldeSlug)
    for folder in folders:
        folder.eliminado = eliminar
        folder.save()
        File.objects.filter(fileinfolder__parent_folder_id = folder.id).update(eliminado = eliminar)
        setEliminarHijos(folder.slug,eliminar)
      
@transaction.atomic        
def setDestruirHijos(foldeSlug):
    rutaFile = settings.MEDIA_ROOT+'files/'
    folderResult = Folder.objects.get(slug = foldeSlug)
    files = File.objects.filter(fileinfolder__parent_folder_id = folderResult.id)
    for file in files:
        os.remove(os.path.join(rutaFile+file.documento_file.name))
    File.objects.filter(fileinfolder__parent_folder_id = folderResult.id).delete()
    folders = Folder.objects.filter(carpeta_hija__parent_folder__slug = foldeSlug)
    for folder in folders:
        setDestruirHijos(folder.slug)    
        folder.delete()
        
def createFolder(nombreFolder,userId,unidadAreaId,padreId):
    folderCreate = Folder.objects.create( 
        slug = get_random_string(11),
        nombre = nombreFolder,
        unidadArea_id = unidadAreaId,
        scope = False,
        user_id = userId

    )
    FolderInFolder.objects.create(
        child_folder_name = folderCreate.nombre,
        child_folder_id = folderCreate.id,
        parent_folder_id = padreId
    )
    return folderCreate
@transaction.atomic
def clonarCarpetaCompartida(foldeSlug,user,padreId):
    rutaFile = settings.MEDIA_ROOT+'files/'
    folderActual = Folder.objects.get(slug = foldeSlug)
    #creando folder padre
    folderPadreCreate = createFolder(folderActual.nombre,user.id,user.unidadArea_id,padreId)
    files = File.objects.filter(fileinfolder__parent_folder_id = folderActual.id)
    for file in files:

        fileObject = open(rutaFile+file.documento_file.name, 'rb')
        fs = FileSystemStorage(location=rutaFile)
        fileSave = fs.save(file.documento_file.name,fileObject)
        nameNewFile = fs.get_valid_name(fileSave)

        fileCreate = File.objects.create(slug = get_random_string(11),
                            nombreDocumento = file.nombreDocumento,
                            contenidoOCR = file.contenidoOCR,
                            documento_file = nameNewFile,
                            extension = file.extension,
                            user_id=user.id,
                            scope=False,
                            unidadArea_id=user.unidadArea_id)
        FileInFolder.objects.create(file_id = fileCreate.id,parent_folder_id = folderPadreCreate.id)
    folders = Folder.objects.filter(carpeta_hija__parent_folder__slug = foldeSlug)
    for folder in folders:
        
        if Folder.objects.filter(carpeta_hija__parent_folder__slug = folder.slug):
            clonarCarpetaCompartida(folder.slug,user,folderPadreCreate.id)
        else:
            createFolder(folder.nombre,user.id,user.unidadArea_id,folderPadreCreate.id)

def validarPrivado(modelo,userId,is_file = False):
    if is_file:
        if modelo.scope ==False:
            if not(modelo.user_id == userId):
                #devolver True por que el file esta oculto
                return True
        folder = Folder.objects.filter(fileinfolder__file = modelo).first()
    else:
        folder = modelo
        
    privado = False
    padrePrivate = obtenerRuta(folder.id,[folder.nombre],True,False,True,userId)
    if padrePrivate:
        privado = True
    elif folder.scope == False:
        if not(folder.user_id == userId):
            privado = True
    return privado
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
        if(sistema == "Windows"):
            pages = convert_from_path(
                absURl,
                thread_count=8,
                poppler_path=config('POPPLER_PATH_WINDOWS')
            )
        else:
            pages = convert_from_path(
                absURl,
                thread_count=8
            )

        image_counter = 1
        imagenesRutas = []
        for page in pages:
            filename = get_random_string(length=40) + ".jpg"
            imagenesRutas.append(filename)
            page.save(settings.MEDIA_ROOT+'test/'+filename, 'JPEG')
            image_counter = image_counter + 1
        #del pages
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
            #print(str(round(percent,2)) + " %")
            textGenerado += text
        
        
        print('contenido extraido por el OCR exitosamente!')
        return textGenerado
        #return 'test'