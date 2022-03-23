import pytesseract

custom_config = r'--oem 3 --psm 6'


def ocr(img, tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    return pytesseract.image_to_string(img, config=custom_config, lang="vie").strip()
