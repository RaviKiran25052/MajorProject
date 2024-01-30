import os
import easyocr
import pyttsx3
import cv2
from gtts import gTTS
import speech_recognition as sr
from langchain.llms import OpenAI
import pytesseract as pytesseract
from googletrans import Translator,LANGUAGES
from langchain.prompts import PromptTemplate

mykey = "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"
model = OpenAI(temperature=0.5, openai_api_key=mykey, model="gpt-3.5-turbo-instruct")

engine = pyttsx3.init()
engine.runAndWait()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

translator = Translator()
pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Ravi\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"

def summarize(text, lang):
    prompt = PromptTemplate(
        template = "give the text in {x} by summarizing the below text, within 50 to 60 words. text: {y}.",
        # template = "summarize this text within 30 words which was in {x}. text: {y}.",
        input_variables = ["x", "y"]
    )
    query = prompt.format(x=lang, y=text)
    translated_text = model(prompt=query)    
    return translated_text

def identifyLang(img):
    
    percentages = []
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
    langCode = max_pair[0]
    if langCode == 'en':
        return [langCode]
    else:
        return ['en',langCode]

def V2T():
    camera=cv2.VideoCapture(0)

    while True:
        _,image=camera.read()
        cv2.imshow('image',image)
        if cv2.waitKey(1)& 0xFF==ord('s'):
            cv2.imwrite('capture.png',image)
            break
    camera.release()
    cv2.destroyAllWindows()
    
    I2T('capture.png')
    
def I2T(img_path):
    
    # langCodes = identifyLang(img_path)
    # reader = easyocr.Reader([langCodes])
    reader = easyocr.Reader(['en','hi'])
    result = reader.readtext(img_path)
    text = ' '.join([text[1] for text in result])
    print("The text was :\n" + text)
    
    ex = translator.detect(text)
    detected_lang = LANGUAGES[ex.lang]
    print("\nThe text was in: " + detected_lang)
    
    engine.say("The text was in: " + detected_lang)
    engine.runAndWait()
    
    engine.say("Do you want to translate?")
    engine.runAndWait()
    ch = input("Do you want to translate : ")
    
    if ch == 'y':
        text, lan = T2T(text, ex.lang)
        print("\nTranslated text :\n",text)
        T2S(text, lan)
    elif ch == 'n':
        T2S(text, ex.lang)


def T2S(text,lan):
    length = len(text.split())
    if length > 50:
        print(f"\nThe text contains {length} words.")
        engine.say(f"The text contains {length} words.")
        engine.runAndWait()
        engine.say("Do you want to Summarize : ")
        engine.runAndWait()
        ch = input("Do you want to Summarize : ")
        # print(lan)
        if ch == 'y':
            text = summarize(text, LANGUAGES[lan])
            print("\nThe summarized text is : ",text)
    audio = gTTS(text=text, lang=lan, slow=False)
    engine.say('the audio was saved...!')
    engine.runAndWait()
    audio.save("example.mp3")
    os.system("start example.mp3 tempo 1.5")


def S2T():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print('Say Something...!')
        engine.say("Say Something...!")
        engine.runAndWait()
        audio = r.listen(source)
    print('end')
    try:
        text = r.recognize_google(audio)
        print("\nYour message was : " + text)
        ex = translator.detect(text)
        engine.say("The text was in :"+LANGUAGES[ex.lang])
        engine.runAndWait()
    except sr.UnknownValueError:
        print('could not understand audio...!')
        engine.say("could not understand audio...!")
        engine.runAndWait()
        S2T()
    except sr.RequestError as e:
        print('could not recognize the audio...!', e)
        engine.say("could not recognize the audio...!")
        engine.runAndWait()
        S2T()


def T2T(message, lang):
    trans = Translator()
    engine.say("In which language do you Want to translate....!")
    engine.runAndWait()
    print("\n0 -> Hindi.\n1 -> Telugu.")
    print("2 -> Tamil.\n3 -> English.\n")
    ip = int(input("In with language do you want : "))
    if ip == 0:
        l = "hi"
    elif ip == 1:
        l = "te"
    elif ip == 2:
        l = "ta"
    elif ip == 3:
        l = "en"
    else:
        engine.say("No option..!, try again.")
        engine.runAndWait()
        T2T(message, lang)
    t = trans.translate(message, dest=l, src=lang)

    return t.text, l


def option(a):
    match a:
        case 'l' | 'L':
            I2T("hindi.png")
        case 'v' | 'V':
            V2T()
        case 's' | 'S':
            S2T()
        case 'e' | 'E':
            exit(0)
        case default:
            print('Please enter correct option...!')


while 1:
    print("\n----------------------------------------------\n")
    print("L -> Listen to the image\nV -> Capture the image\nS -> Send a message.\nE -> Escape\n")
    opt = input('Enter your option : ')
    option(opt)
engine.runAndWait()
engine.stop()