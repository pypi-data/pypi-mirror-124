from os import replace
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter,ImageDraw
import pdf2image 
from pytesseract import image_to_string
import pytesseract as tess
tess.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
from pdf2image import convert_from_path
import re
from pydantic import BaseModel
from fastapi import FastAPI


def convert_pdf_to_img(pdf_file):
      return convert_from_path(pdf_file)


def convert_image_to_text(file):

    text = image_to_string(file)
    return text
def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        
        final_text += convert_image_to_text(img)
    final_text=re.sub('[\$,]', '',final_text)
    li= re.findall(r"[-+]?\d*\.\d+|\d+",final_text)
    li1=[]
    for i in li:
     if(i.isdigit()==False):
        li1.append(i)
    li2=list(map(float, li1))
    return max(li2)







 


