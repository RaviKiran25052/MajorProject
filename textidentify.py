import cv2
from PIL import Image
from pytesseract import pytesseract
import easyocr

camera=cv2.VideoCapture(0)

while True:
    _,image=camera.read()
    cv2.imshow('image',image)
    if cv2.waitKey(1)& 0xFF==ord('s'):
        cv2.imwrite('bomma.jpg',image)
        break
camera.release()
cv2.destroyAllWindows()

def identifyLang(img):
    
    percentages = []
    # en - english
    # hi - hindi
    # te - telugu
    # ta - tamil
    # kn - kanada
    # mr - marathi
    codes = ['en','te','hi']

    for code in codes:
        reader = easyocr.Reader([code],gpu=False)
        result = reader.readtext(img)

        pb = 0
        count = 0
        for items in result:
            _,_,score = items
            pb += score
            count +=1
        percentages.append([code, pb/count])
        # print(lang,percentages)
        
    max_pair = max(percentages, key=lambda x: x[1])
    print(max_pair[0])
    

def tesseract():
    path_to_tesseract = "C:\\Users\\Ravi\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"
    image_path = "bomma.jpg"
    pytesseract.tesseract_cmd = path_to_tesseract
    text = pytesseract.image_to_string(Image.open(image_path))
    print(text[:-1])
tesseract()

identifyLang('bomma.jpg')