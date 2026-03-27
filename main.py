import cv2
import re
import requests
from config import CAMERA_INDEX
from database import init_db, enregistrer_acces
from datetime import datetime

# ── Plate Recognizer API ──
PLATE_RECOGNIZER_TOKEN = "38d5d237e58141e475e57b391ae089ce17a677f4"
PLATE_RECOGNIZER_URL   = "https://api.platerecognizer.com/v1/plate-reader/"

def normaliser_chiffres(texte):
    table = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    return texte.translate(table)

def lire_plaque_api(image_path):
    with open(image_path, "rb") as f:
        response = requests.post(
            PLATE_RECOGNIZER_URL,
            headers={"Authorization": f"Token {PLATE_RECOGNIZER_TOKEN}"},
            files={"upload": f}
        )
    if response.status_code == 201:
        data = response.json()
        results = data.get("results", [])
        if results:
            plaque = results[0]["plate"].upper()
            print(f"🌐 Plate Recognizer: {plaque}")
            return plaque
    print(f"⚠️  API erreur: {response.status_code} - {response.text}")
    return None

def formater_plaque_tunisienne(plaque_brute):
    if not plaque_brute:
        return None
    plaque = normaliser_chiffres(plaque_brute.strip())
    if "تونس" in plaque or "نت" in plaque:
        return plaque
    chiffres = re.sub(r"[^\d]", "", plaque)
    print(f"🔢 Chiffres extraits: {chiffres}")
    n = len(chiffres)
    if n == 7:
        return f"{chiffres[:3]} تونس {chiffres[3:]}"
    if n == 6:
        return f"{chiffres} نت"
    if n == 5:
        return f"{chiffres} نت"
    if n == 8:
        return f"{chiffres[:2]} {chiffres[2:]}"
    return chiffres if chiffres else None

def extraire_matricule(image_path):
    plaque_brute = lire_plaque_api(image_path)
    if plaque_brute:
        return formater_plaque_tunisienne(plaque_brute)
    return None

def main():
    init_db()
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la caméra")
        return

    print("=" * 50)
    print("🚦 GESTION D'ACCÈS VÉHICULES")
    print("=" * 50)
    print("📷 Appuyez sur 'S' pour capturer | 'Q' pour quitter")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera - Detection Matricule", frame)
        key = cv2.waitKey(1)

        if key == ord('s') or key == ord('S'):
            img_path = "capture.jpg"
            cv2.imwrite(img_path, frame)
            cap.release()
            cv2.destroyAllWindows()

            matricule = extraire_matricule(img_path)
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
