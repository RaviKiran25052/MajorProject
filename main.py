from PIL import Image
import pytesseract
import moviepy.editor as mp

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Ravi\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"

def extract_text_from_video():
    print(' the video path to extract text from it ')
    try:
        video_path = input(' [+] Your video path : ')
        video_clip = mp.VideoFileClip(video_path)
        n_frames = int(video_clip.fps * video_clip.duration)

        text_file = open(video_path.split('.')[0] + '.txt', 'x')

        for i in range(n_frames):
            frame = video_clip.get_frame(i)
            image = Image.fromarray(frame)
            text = pytesseract.image_to_string(image)
            text_file.writelines(text.strip())

    except Exception as e:
        print(e)

extract_text_from_video()
