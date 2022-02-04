from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
from django.conf import settings

import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

class DocumentoOCR():
    PDF_file = None
    def __init__(self,ruta):
        self.PDF_file = ruta
    
    def obtenerTexto(self):
        doc = self.PDF_file[6:]
        absURl = settings.MEDIA_ROOT.replace("\\","/")  + doc
        print('obteniendo texto de ' + absURl.replace("/","\\"))
        pages = convert_from_path(absURl.replace("/","\\"), 500, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
        image_counter = 1
        for page in pages:

            filename = "page_"+str(image_counter)+".jpg"
            page.save(filename, 'JPEG')
            image_counter = image_counter + 1
        

        filelimit = image_counter-1
        #outfile = "out_text.txt"
        #f = open(outfile, "a")
        textGenerado = ""

        for i in range(1, filelimit + 1):
            filename = "page_"+str(i)+".jpg"
            # Recognize the text as string in image using pytesserct
            text = str(((pytesseract.image_to_string(Image.open(filename)))))

            text = text.replace('-\n', '')    
        
            #f.write(text)
            textGenerado += text

        #f.close()
        return textGenerado