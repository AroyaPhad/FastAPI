import pytesseract
import os
import re

async def extract_info_from_text(text):
    lines = text.split("\n")
    
    student_id_text = ""


    id_pattern = r'(\d{13})'

    for line in lines:
        if not student_id_text:
            student_id_match = re.search(id_pattern, line)
            if student_id_match:
                student_id_text = student_id_match.group()

    return student_id_text

async def read_image(img_path, lang='eng'):
    try:
        text = pytesseract.image_to_string(img_path, lang=lang)
        student_id = await extract_info_from_text(text)
        return student_id
    except Exception as e:
        return "[ERROR] Unable to process file"
