import cv2
import easyocr
import re
from config import LANGUES_OCR, CAMERA_INDEX
from database import init_db, enregistrer_acces
from datetime import datetime

reader = easyocr.Reader(LANGUES_OCR, gpu=False)

def traiter_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    resultats = reader.readtext(thresh, detail=0)
    texte = " ".join(resultats)
    print(f"🧾 OCR: {resultats}")

    chiffres = re.findall(r"\d+", texte)
    tous_chiffres = "".join(chiffres)
    a_nt    = "نت" in texte
    a_tunis = "تونس" in texte

    # Accepter uniquement نت ou تونس
    if a_nt and tous_chiffres:
        return f"{tous_chiffres} نت"

    if a_tunis and len(chiffres) >= 2:
        return f"{chiffres[0]} تونس {chiffres[1]}"

    if a_tunis and len(tous_chiffres) >= 5:
        return f"{tous_chiffres[:3]} تونس {tous_chiffres[3:]}"

    print("❌ Matricule refusé : ni نت ni تونس détecté")
    return None

def afficher_ocr(image):
    try:
        results = reader.readtext(image)
        for (bbox, text, prob) in results:
            tl = tuple(map(int, bbox[0]))
            br = tuple(map(int, bbox[2]))
            cv2.rectangle(image, tl, br, (0,255,0), 2)
            cv2.putText(image, text, tl, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        cv2.imshow("OCR Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print("⚠️ Erreur affichage OCR :", e)

def main():
    init_db()

    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la caméra")
        return

    print("=" * 60)
    print("🚦 SYSTÈME DE GESTION D'ACCÈS VÉHICULES")
    print("=" * 60)
    print("📷 Appuyez sur 'S' pour capturer | 'Q' pour quitter")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Camera - Detection Matricule", frame)
        key = cv2.waitKey(1)

        if key == ord('s') or key == ord('S'):
            cv2.imwrite("capture.jpg", frame)
            print("\n💾 Image capturée")
            cap.release()
            cv2.destroyAllWindows()

            afficher_ocr(frame)
            matricule = traiter_image(frame)

            if matricule:
                date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                statut = "AUTORISÉ"
                enregistrer_acces(matricule, date_heure, statut)
                print(f"\n✅ Matricule : {matricule}")
                print(f"📅 Date      : {date_heure}")
                print(f"✓  Statut    : {statut}")
                print("💾 Enregistré! Rafraîchissez le dashboard.")
            else:
                print("\n❌ Aucun matricule détecté")
            return

        if key == ord('q') or key == ord('Q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()