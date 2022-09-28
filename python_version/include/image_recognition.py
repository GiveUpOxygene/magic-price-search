import cv2 as cv
import numpy as np
import pytesseract as pt
from PIL import Image

pt.pytesseract.tesseract_cmd = r'C:\Users\alexandre\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

cam = cv.VideoCapture(0)

# nom_fenetre = "Test"
# largeur_image = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
# hauteur_image = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))

# cv.namedWindow(nom_fenetre, cv.WINDOW_AUTOSIZE)
image_path  = r'void_grafter.png'
string_image = pt.image_to_string(Image.open(image_path))
print(string_image)
# not_found = True
print(type(pt.image_to_string(string_image, lang='fra')))

# while not_found == True:
#     ret, image = cam.read()
#     if ret:
#         image = cv.flip(image,1)
#         cv.imshow(nom_fenetre, image)
#         print(type(pt.image_to_string(pt.image_to_string(image), lang='fra')))
#         if cv.waitKey(25) & 0xFF == ord('q'):
#             break