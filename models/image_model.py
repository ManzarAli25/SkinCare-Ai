from transformers import pipeline

def classify_image(image):
    pipe = pipeline("image-classification", model="imfarzanansari/skintelligent-acne")
    return pipe(image)
