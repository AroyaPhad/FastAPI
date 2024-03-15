import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from io import BytesIO
from mtcnn.mtcnn import MTCNN
import pytesseract
import re

siamese_model = tf.keras.models.load_model('/Users/bubu/Desktop/fastapi/siamese_model_vgg4.h5')

async def extract_info_from_text(text):
    try:
        student_id_text = ""

        lines = text.split("\n")
        id_pattern = r'(\d{13})'

        for line in lines:
            if not student_id_text:
                student_id_match = re.search(id_pattern, line)
                if student_id_match:
                    student_id_text = student_id_match.group()


            if student_id_text:
                break
        return student_id_text
    except Exception as e:
        return str(e)


async def read_image(img_path, lang='eng'):
    try:
        text = pytesseract.image_to_string(img_path, lang=lang)
        student_id, name = await extract_info_from_text(text)
        return student_id, name
    except Exception as e:
        return str(e)

def load_and_preprocess_image(image_np, target_size=(224, 224)):
    # Check if the image is loaded successfully
    if image_np is None:
        print("Error: Unable to load image.")
        return None
    
    # Check the size of the loaded image
    print("Loaded image shape:", image_np.shape)
    
    # Resize the image to the target size
    image = cv2.resize(image_np, target_size)
    # Normalize the image
    image_normalized = image / 255.0
    return image_normalized

def detect_and_crop_faces(image_np):
    detector = MTCNN()  # Instantiating the MTCNN detector here

    data = image_np
    faces = detector.detect_faces(data)

    if len(faces) > 0:
        x, y, width, height = faces[0]['box']
        x1, y1 = x, y
        x2, y2 = x1 + width, y1 + height
        cropped_face = data[y1:y2, x1:x2]
        return cropped_face
    else:
        return None

async def main():
    st.title('Face Comparison App')

    # File uploader for ID photo
    id_photo = st.file_uploader('Upload ID Photo', type=['jpg', 'png'])

    # File uploader for selfie
    selfie = st.file_uploader('Upload Selfie', type=['jpg', 'png'])

    if id_photo and selfie:
        # Convert uploaded images to PIL Image objects
        id_photo_pil = Image.open(BytesIO(id_photo.read()))
        selfie_pil = Image.open(BytesIO(selfie.read()))

        # Convert PIL Images to numpy arrays
        id_photo_np = np.array(id_photo_pil)
        selfie_np = np.array(selfie_pil)

        id_cropped_face = detect_and_crop_faces(id_photo_np)
        selfie_cropped_face = detect_and_crop_faces(selfie_np)

        id_image = load_and_preprocess_image(id_cropped_face)
        selfie_image = load_and_preprocess_image(selfie_cropped_face)

        image_pairs = [(id_image, selfie_image)]

        image_pairs = np.array(image_pairs)

        if id_image is not None and selfie_image is not None:
            score = siamese_model.predict([image_pairs[:, 0, :], image_pairs[:, 1, :]])

            st.image(id_image, caption='ID Photo', width=200)
            st.image(selfie_image, caption='Selfie', width=200)

            average_similarity_score = np.mean(score)
            st.write(score)

            if average_similarity_score >= 0.6:
                st.write("same person.")

                st.write("different persons.")
        
            # student_id, name = await read_image(id_photo_pil)

            # st.write("Student ID:", student_id)
            # st.write("Name:", name)
        else:
            st.write("No faces detected in one or both images.")

        

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
