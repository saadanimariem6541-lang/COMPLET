import cv2

cap = cv2.VideoCapture(0)  # index 0 pour la webcam
print("📷 Tentative d'ouverture de la caméra...")

if not cap.isOpened():
    print("❌ Impossible d'ouvrir la caméra. Vérifiez les permissions ou l'index.")
    exit()

ret, frame = cap.read()
if ret:
    print("✅ Caméra ouverte avec succès !")
    cv2.imshow("Test Camera", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("❌ Impossible de lire la caméra")

cap.release()