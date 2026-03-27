import cv2

CAMERA_INDEX = 0  # index de la webcam

def capture_webcam():
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la caméra")
        return None

    print("📷 Caméra activée !")
    print("👉 Appuyez sur 'S' pour capturer l'image")
    print("👉 Appuyez sur 'Q' pour quitter")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Impossible de lire la caméra")
            break

        # Affichage en miroir
        frame_mirror = cv2.flip(frame, 1)

        cv2.imshow("Webcam - Capture", frame_mirror)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            # Sauvegarder l'image capturée
            cv2.imwrite("capture.jpg", frame_mirror)
            print("💾 Image capturée avec succès : capture.jpg")
            cap.release()
            cv2.destroyAllWindows()

            return frame_mirror
        if key == ord('q'):
            print("❌ Fermeture de la caméra")
        cap.release()
        cv2.destroyAllWindows()
        return None


    capture_webcam()