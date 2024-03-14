import cv2
import pytesseract

async def rois_and_ocr(image):
    width, height = 1048, 654
    resized_image = cv2.resize(image, (width, height))
    
    rois = [
        ((453, 223), (782, 267), 'student_id'),
        ((82, 539), (755, 597), 'name'),
    ]
    
    roi_texts = {}
    
    for i, (top_left, bottom_right, roi_name) in enumerate(rois, start=1):
        x_start, y_start = top_left
        x_end, y_end = bottom_right
        
        roi = resized_image[y_start:y_end, x_start:x_end]
        
        text = pytesseract.image_to_string(roi, config='--psm 6')
        roi_texts[roi_name] = text
        
    return roi_texts.get('student_id'), roi_texts.get('name')
