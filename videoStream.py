from PIL import Image
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Ravi\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"

def extract():
    
    print('Press "s" to stop the webcam and start text extraction.')
    cap = cv2.VideoCapture(0)

    text_file = open('output_text.txt', 'w')

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            cv2.imshow('Webcam', frame)
            image = Image.fromarray(frame)
            text = pytesseract.image_to_string(image)
            text_file.write(text)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()

    text_file.close()

    print('Text extraction completed. Check "output_text.txt" for the result.')

extract()
