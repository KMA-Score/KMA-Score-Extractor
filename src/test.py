import cv2
from pdf2image import convert_from_path
from tqdm import tqdm
import os
import pytesseract
import matplotlib.pyplot as plt

pytesseract.pytesseract.tesseract_cmd = r'E:\PROJECT\KMA\iKMA\pdfScanner\bin\tesseract\windows\tesseract.exe'
poppler_path = os.path.join(os.path.abspath(".."), "bin", "poppler-22.01.0", "Library", "bin")

if __name__ == "__main__":
    # images = convert_from_path("../sample/test.pdf", poppler_path=poppler_path)
    #
    # for i in tqdm(range(len(images))):
    #     # images[i].save('temp/pdfImage/' + str(i) + '.jpg', 'JPEG')
    #     images[i].save('../temp/images/' + str(i) + '.jpg', 'JPEG')
    # pass

    img = cv2.imread("../temp/pdf2images/87.jpg")

    custom_config = r'--oem 3 --psm 6'

    # Start coordinate, here (5, 5)
    # represents the top left corner of rectangle
    start_point = (1360, 95)

    # Ending coordinate, here (220, 220)
    # represents the bottom right corner of rectangle
    end_point = (1650, 145)
    color = (255, 0, 0)
    thickness = 1

    img = cv2.rectangle(img, start_point, end_point, color, thickness)

    # img = img[90:145, 150:335] #HVKTMM
    # yy xx
    # img = img[315:365, 230:900] #Subject Name

    img = img[315:365, 1360:1650] # subject code

    # img = img[95:150, 35:250] # hoc phan

    # img = img[95:145, 1360:1650] # ma hoc phan page 2

    a = pytesseract.image_to_string(img, config=custom_config, lang="vie")
    print(a.strip())

    plt.imshow(img)

    # display that image
    plt.show()
