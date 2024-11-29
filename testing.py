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
img = cv2.imread('./Images/par7.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
val, tre = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
result = pytesseract.image_to_data(tre, lang='pol', output_type=Output.DICT)
img, listy = markPicture(result, img)
window = 'Paragon'
cv2.namedWindow(window, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window, 1000,1000)
cv2.imshow(window, img)
cv2.imshow('tre', tre)
cv2.waitKey(0)

#print(list[5].article, list[5]. price)
#print(listy)
    

