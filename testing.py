from ocr_func import markPicture, showReceipt
import os
import pytesseract
import cv2
import numpy as np
from pytesseract import Output
from divider import DataPoint, Receipt


#! Ustawienie katalogu roboczego na katalog skryptu -> pozwala na wstawianie relatywnych ścieżek do plików
#*#####################################
script_dir = os.path.dirname(__file__) 
os.chdir(script_dir)
#*#####################################

list = []
img = cv2.imread('./Images/par1.png')
result = pytesseract.image_to_data(img, lang='pol', output_type=Output.DICT)
img, list = markPicture(result, img)
#cv2.imshow('Paragon', img)
#cv2.waitKey(0)

print(list[5].article, list[5]. price)
    

