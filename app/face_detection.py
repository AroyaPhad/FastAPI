from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN

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