from flask import request

def read_uploaded_image():
    if "image" not in request.files:
        return {"error": "No image file"}
    file = request.files["image"]

    pass