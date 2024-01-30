import easyocr

img_path = 'telugu.png'

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
            _,text,score = items
            pb += score
            count +=1
            print(text)
        percentages.append([code, pb/count])
        # print(lang,percentages)
        
    max_pair = max(percentages, key=lambda x: x[1])
    print(max_pair[0])
    
# identifyLang('test1.jpg')