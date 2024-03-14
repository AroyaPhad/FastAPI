from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import ocr
import os
import shutil

from fastapi.responses import StreamingResponse

from face_detection import detect_and_crop_faces
from load_process import load_and_preprocess_image
from rois import rois_and_ocr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""],
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=["*"],
)

siamese_model = tf.keras.models.load_model('/Users/bubu/Desktop/fastapi/siamese_model_vgg4.h5')


def compare_images(id_image, selfie_image):
    image_pairs = [(id_image, selfie_image)]
    image_pairs = np.array(image_pairs)
    score = siamese_model.predict([image_pairs[:, 0, :], image_pairs[:, 1, :]])
    return score


@app.post("/filters/detect_and_crop_faces/")
async def detect_faces(image: UploadFile = File(...)):
    contents = await image.read()
    image_np = np.frombuffer(contents, dtype=np.uint8)
    pixels = np.array(Image.open(io.BytesIO(contents)))
    cropped_face = detect_and_crop_faces(pixels)

    if cropped_face is not None:

        img_bytes = io.BytesIO()
        Image.fromarray(cropped_face).save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        return StreamingResponse(io.BytesIO(img_bytes), media_type="image/jpeg")
    else:
        return JSONResponse(content={"message": "No faces detected in the image."})


#-------------------------------------------------------------------------------------------


@app.post("/api/v1/extract_text")
async def extract_text(image: UploadFile = File(...)):
    temp_file = _save_file_to_disk(image, path="temp", save_as="temp")
    text = await ocr.read_image(temp_file)
    return {"filename": image.filename, "text": text}

def _save_file_to_disk(uploaded_file, path=".", save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path, save_as + extension)
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return temp_file


#-------------------------------------------------------------------------------------------


@app.post('/verify')
async def faces_recognition(id_photo: UploadFile = File(...), selfie: UploadFile = File(...)):
    contents1 = await id_photo.read()
    contents2 = await selfie.read()
    
    id_photo_im = np.array(Image.open(io.BytesIO(contents1)))
    selfie_im = np.array(Image.open(io.BytesIO(contents2)))

    id_cropped_face = detect_and_crop_faces(id_photo_im)
    selfie_cropped_face = detect_and_crop_faces(selfie_im)

    if id_cropped_face is not None and selfie_cropped_face is not None:
        id_image = load_and_preprocess_image(id_cropped_face)
        selfie_image = load_and_preprocess_image(selfie_cropped_face)

        score = compare_images(id_image, selfie_image)
        average_similarity_score = np.mean(score)

        student_id, name = await rois_and_ocr(id_photo_im)
        student_id = student_id.strip().replace(" ", "")

        if average_similarity_score >= 0.6:
            result = "same person."
            is_verified = True
        else:
            result = "different persons."
            is_verified = False
    else:
        result = "No faces detected in one or both images."
        is_verified = False

    return {
        "vetify": bool(is_verified),
        "result": result,
        "score": float(average_similarity_score),
        "student_id": student_id,
        "name": name.strip()
    }