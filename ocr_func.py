import numpy as np
import pytesseract
import cv2
from PIL import Image, ImageFont, ImageDraw
from pytesseract import Output
import os
import re #? Regular Expresions
from divider import DataPoint

#! Ustawienie katalogu roboczego na katalog skryptu -> pozwala na wstawianie relatywnych ścieżek do plików
#*#####################################
script_dir = os.path.dirname(__file__) 
os.chdir(script_dir)
#*#####################################

#! Wzór do używania regularnych wyrażeń, w tym przypadku dla cen:
# Wzór dla cen, gdzie separator dziesiętny może być kropką lub przecinkiem 
price_pattern = r'\d{1,}[.,]\d{2}'
# Wzór dla nazw składających się jedynie z liter 
name_pattern = r'^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]{2,}$'

#? Czcionka do użycia
fontCalibri = './Materials/calibri.ttf'

#! Funkcja do rysowania prostokąta wokół znalezionego tekstu
#* result -> Output.DICT obrazka z informacjami o nim
#* img -> oryginalny obrazek
#* pos -> pozycja słowa na liście wokół której będziemy rysować
#* color -> kolor prostokąta, wstępnie czerwony (mam nadzieję)
def outlineBox(result, img, pos, color=(0,0,255)):
    x = result['left'][pos]   #? współrzędna x (startowa) słowa (od lewej)
    y = result['top'][pos]    #? współrzęda y (startowa) słowa (od góry)
    w = result['width'][pos]  #? szerokość na jaką rozciąga się słowo
    h = result['height'][pos] #? wysokość na jaką rozciąga się słowo

    cv2.rectangle(img, (x,y), (x+w, y+h), color, 2) #? obrys słowa (2 - grubość lini)

    return x,y,img #? zwracamy nowy obraz i współrzędne

#! Funkcja do nakładania tekstu z innego języka za pomocą PIL
def writeText(text, x, y, img, fontType, font_size = 12, color_text=(255, 0, 0)):
    font = ImageFont.truetype(fontType, font_size)
    img_pil = Image.fromarray(img) #Konwersja obrazka z cv2
    draw = ImageDraw.Draw(img_pil)
    draw.text((x, y - font_size), text, font = font, fill=color_text)
    img = np.array(img_pil) #Konwersja  na typ obrazka cv2
    return img


#! Funkcja do nakładania widocznego tekstu na obrazek połączona z obrysowywaniem słów
#* result -> Output.DICT obrazka z informacjami o nim
#* img -> oryginalny/przetworzony obrazek
#* min_confidance -> minimalny poziom ufności, od którego uznajemy słowo (opcjonalnie)
#* color_outline -> kolor obrysu BGR (opcjonalnie)
#* color_text -> kolor tekstu tekstu na obrazie BGR (opcjonalnie)
def markPicture(result: Output, img, min_confidence = 20, color_outline = (0,0,255), color_text = (255,0,0)):
    lista = [] 
    name = ""
    price = ""
    for i in range(0, len(result['text'])):
        
        confidence = int(result['conf'][i]) #? Poziom pewności odczytanego słowa z pozycji i

        if confidence > min_confidence: #? Sprawdzamy z jakim prawdopodobieństwem jest to słowo

            text = result['text'][i] #? Zwracamy słowo

            if not text.isspace() and len(text) > 0: #? Sprawdzamy, czy nie jest to przypadkiem spacja (blank space)

                if re.match(name_pattern, text) and result['top'][i] > img.shape[0]/5 and result['top'][i] < img.shape[0] - 100:
                    x,y,img = outlineBox(result, img, i, (255,0,255)) 
                    img = writeText(text, x, y, img, fontCalibri) #? Nadpisuje tekst na obrazie
                    name = text

                if re.match(price_pattern, text) and result['left'][i] > img.shape[1]/2 : #? Sprawdzamy, czy dany tekst wpisuje się w schemat
                    x,y,img = outlineBox(result, img, i, (0,255,0)) #? Zakreślamy ten tekst na zielono
                    img = writeText(text, x, y, img, fontCalibri) #? Nadpisuje tekst na obrazie
                    price = text
                new_data = DataPoint(name, price)
                lista.append(new_data)
    return img, lista


#! Funkcja do pokazywania oznaczeń na podanym paragonie
def showReceipt(name: str):
    root = './Images/' + name       #? Ścieżka
    img = cv2.imread(root)          #? Odczytanie pliku
    if img is None: 
        raise FileNotFoundError(f"Nie znaleziono pliku: {root}")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     #? Zmiana na skalę szarości
    value, treshIMG = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY  | cv2.THRESH_OTSU) #? Tresholding
    result = pytesseract.image_to_data(treshIMG, lang = 'pol', output_type = Output.DICT)
    img = cv2.cvtColor(treshIMG, cv2.COLOR_GRAY2BGR)
    markedIMG = markPicture(result, img)
    cv2.imshow('Marked', markedIMG)
    cv2.waitKey(0)
    return markedIMG
