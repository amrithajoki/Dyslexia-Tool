if __name__ == "__main__": main()
import cv2
import pytesseract
from piper import PiperVoice
import sounddevice as sd
import numpy as np
import io
import wave
import re

# ===================== CONFIG =====================
IMAGE_PATH = r"/home/mypi/Music/captured_image.jpg"

# Map languages to Piper models and Tesseract codes
LANG_CONFIG = {
    "en": {"tess": "eng", "model": r"en_US-amy-low.onnx"},
    "hi": {"tess": "hin", "model": r"hi_IN-rohan-medium.onnx"},
    "te": {"tess": "tel", "model": r"te_IN-venkatesh-medium.onnx"},
    "ml": {"tess": "mal", "model": r"ml_IN-arjun-medium.onnx"},
}

DEFAULT_LANG = "en"

# ===================== MODULE 1: IMAGE READING =====================
def load_image(image_path: str):
    """Reads image from disk and converts to grayscale."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

# ===================== MODULE 2: AUTO LANGUAGE DETECTION =====================
def detect_script_and_language(gray_image) -> str:
    """
    Runs OCR for all languages and detects the language robustly using character counts.
    """
    text_all = pytesseract.image_to_string(
        gray_image, lang="eng+hin+tel+mal"
    ).strip()
    print("🔎 Initial OCR Text for Detection:\n", text_all)

    # Count characters for each script
    counts = {
        "hi": len(re.findall(r'[\u0900-\u097F]', text_all)),    # Hindi
        "te": len(re.findall(r'[\u0C00-\u0C7F]', text_all)),    # Telugu
        "ml": len(re.findall(r'[\u0D00-\u0D7F]', text_all)),    # Malayalam
        "en": len(re.findall(r'[A-Za-z]', text_all)),            # English
    }
