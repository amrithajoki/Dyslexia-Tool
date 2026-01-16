from picamera2 import Picamera2, Preview
import time
import cv2

def main():
    picam = Picamera2()

    # Configure preview
    preview_config = picam.create_preview_configuration(main={"size": (640, 480)})
    picam.configure(preview_config)

    picam.start_preview(Preview.QTGL)
    picam.start()

    print("📷 Camera preview started.")
    print("Press 'c' + Enter to capture an image, 'q' + Enter to quit.")

    while True:
        key = input("Enter command: ")

        if key.lower() == 'c':
            # Capture image using Picamera2
            frame = picam.capture_array()
            filename = "captured_image.jpg"
            cv2.imwrite(filename, frame)
            print(f"✅ Image captured and saved as '{filename}'")

        elif key.lower() == 'q':
            break

    picam.stop_preview()
    picam.stop()
    print("🛑 Camera stopped.")

