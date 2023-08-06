#C:\Users\Admin\OneDrive\Desktop\virtualenv\har
from PIL import Image
from pdf2image import convert_from_path
import pytesseract as tess
import re
images = convert_from_path('invoice_1.pdf',500,poppler_path=r'C:\Users\Admin\OneDrive\Desktop\poppler-21.10.0\Library\bin')#replace paths
images[0].save('invoice_1.png','JPEG')#replace image name
tess.pytesseract.tesseract_cmd='C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe' #replace path
image = Image.open('invoice_1.png')#replace name
image_to_text =tess.image_to_string(image, lang='eng') 
print(image_to_text)
res=image_to_text.split()
fl=[]
regex = '[+-]?[0-9]+\.[0-9]+'
for s in res:
      if(re.search(regex, s)): 
         fl.append(s)
print(max(fl))
