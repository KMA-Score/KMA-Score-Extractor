import easyocr

reader = easyocr.Reader(['vi', 'en'])


def ocr(img):
    text = reader.readtext(img, detail=0)
    text = " ".join(text)

    return text
