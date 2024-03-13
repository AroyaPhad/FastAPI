import cv2

def load_and_preprocess_image(image_np, target_size=(224, 224)):
    image = cv2.resize(image_np, target_size)
    # Normalize the image
    image_normalized = image / 255.0
    return image_normalized