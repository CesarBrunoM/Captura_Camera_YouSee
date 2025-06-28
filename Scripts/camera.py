import cv2
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()

STREAM_URL = os.getenv("STREAM_URL")

def get_stream():
    logger.info("Iniciando captura de vídeo...")
    cap = cv2.VideoCapture(STREAM_URL)
    if not cap.isOpened():
        logger.error("Não foi possível abrir o stream RTSP")
        raise Exception("Não foi possível abrir o stream RTSP")
    logger.info("Stream conectado com sucesso.")
    return cap

def detect_motion(frame1, frame2, min_area=500):
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    motion_detected = any(cv2.contourArea(c) > min_area for c in contours)
    if motion_detected:
        logger.info("Movimento detectado!")
    return motion_detected