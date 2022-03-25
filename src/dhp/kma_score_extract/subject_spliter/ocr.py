import easyocr


def ocr(img, gpu=True):
    reader = easyocr.Reader(['vi', 'en'], gpu=gpu)
    text = reader.readtext(img, detail=0)
    text = " ".join(text)

    return text
