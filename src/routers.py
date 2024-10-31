from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
import base64


router = APIRouter()
CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


@router.get("/healthcheck")
async def healthcheck():
    return {"message": "OK"}


@router.post("/extract")
async def extract(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(BytesIO(image_bytes))
    image_data = np.array(image)

    gray_scale_image = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
    detected_face = CASCADE.detectMultiScale(gray_scale_image, 1.1, 4)

    if not detected_face.any():
        return {"message": "No face detected"}

    x, y, w, h = detected_face[0]
    face = image_data[y : y + h, x : x + w]
    _, image_buffer = cv2.imencode(".jpg", face)
    encoded_image = base64.b64encode(image_buffer).decode("utf-8")

    return {"image": encoded_image}
