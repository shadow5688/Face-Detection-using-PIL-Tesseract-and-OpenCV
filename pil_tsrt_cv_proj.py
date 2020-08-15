from zipfile import ZipFile
import PIL
from PIL import Image
import pytesseract
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

name = input("Enter name to be searched: ")
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

zip_file = ZipFile("./small_img.zip")
for img_name in zip_file.namelist():
    print("Scanning " + img_name)
    with zip_file.open(img_name) as paper_img:
        pil_paper_img = Image.open(paper_img)
        text = pytesseract.image_to_string(pil_paper_img)
        if name in text:
            print("Found '{}' in image {}".format(name, img_name))
            images = []
            numpy_image = np.array(pil_paper_img)
            img_raw=cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
            gray_img = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray_img, 1.35, 4)
            size = (273, 273)
            for (x, y, w, h) in faces:
                croped_img = img_raw[y:y+h, x:x+w]
                croped_img = cv2.resize(croped_img, size)
                images.append(croped_img)
            images_pil = []

            for img in images:
                img_pl = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                images_pil.append(img_pl)

            first_image=images_pil[0]
            contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*5,first_image.height*3))
            x=0
            y=0
            for img in images_pil:
                contact_sheet.paste(img, (x, y) )
                if x+first_image.width == contact_sheet.width:
                    x=0
                    y=y+first_image.height
                else:
                    x=x+first_image.width

            # resize and display the contact sheet
            contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
            contact_sheet.show()


#Christopher
#Mark