import cv2
from camera import get_stream, detect_motion
from recorder import start_recording
from uploader import upload_to_drive

cap = get_stream()
ret, frame1 = cap.read()
ret, frame2 = cap.read()

out = None
filename = None

print("Iniciando monitoramento...")

try:
    while True:
        if detect_motion(frame1, frame2):
            print("Movimento detectado! Gravando...")
            if out is None:
                out, filename = start_recording(frame1)

            out.write(frame1)

        frame1 = frame2
        ret, frame2 = cap.read()
        if not ret:
            break

        cv2.imshow("Monitoramento", frame1)
        if cv2.waitKey(1) == 27:
            break
finally:
    if out:
        out.release()
        print(f"Gravação salva em: {filename}")
        #upload_to_drive(filename)
    cap.release()
    cv2.destroyAllWindows()