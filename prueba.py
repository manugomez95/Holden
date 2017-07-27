from PIL import Image
from pytesseract import *
import numpy

pil_im = Image.open('/home/manuel/Descargas/A.png')
pil_im = pil_im.convert('1', dither=Image.NONE)
pil_im = pil_im.convert('RGB')

cv_im = numpy.array(pil_im) 
# Convert RGB to BGR 
cv_im = cv_im[:, :, ::-1].copy() 

c1 = 25
r1 = 0
cv_im = cv_im[c1:c1+150,r1:r1+150]

pil_im = Image.fromarray(cv_im)
pil_im.show()

text = image_to_string(pil_im, config='-psm 10')
print text
