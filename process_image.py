import cv2
import easyocr
import re
from database import init_db, enregistrer_acces
from config import LANGUES_OCR
from datetime import datetime

reader = easyocr.Reader(LANGUES_OCR, gpu=False)

def extraire_depuis_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ Image non trouvée : {image_path}")
        return None

    r1 = reader.readtext(img, detail=0)
    print(f"🧾 OCR résultats: {r1}")

    texte = " ".join(r1)
    print(f"📝 Texte détecté: {texte}")

    chiffres = re.findall(r"\d+", texte)
    tous_chiffres = "".join(chiffres)
    a_nt    = "نت" in texte
    a_tunis = "تونس" in texte

    print(f"🔢 Chiffres: {tous_chiffres} | نت: {a_nt} | تونس: {a_tunis}")

    # Accepter uniquement نت ou تونس
    if a_nt and tous_chiffres:
        return f"{tous_chiffres} نت"

    if a_tunis and len(chiffres) >= 2:
        return f"{chiffres[0]} تونس {chiffres[1]}"

    if a_tunis and len(tous_chiffres) >= 5:
        return f"{tous_chiffres[:3]} تونس {tous_chiffres[3:]}"

    print("❌ Matricule refusé : ni نت ni تونس détecté")
    return None

def main():
    init_db()

    print("=" * 60)
    print("🔍 TRAITEMENT DE capture.jpg")
    print("=" * 60)

    matricule = extraire_depuis_image("capture.jpg")

    if matricule:
        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        statut = "AUTORISÉ"

        print(f"\n✅ Matricule : {matricule}")
        print(f"📅 Date      : {date_heure}")
        print(f"✓  Statut    : {statut}")

        enregistrer_acces(matricule, date_heure, statut)
        print(f"\n💾 Enregistré dans la base de données!")
        print("🌐 Rafraîchissez le dashboard pour voir le résultat!")
    else:
        print("\n❌ Aucun matricule détecté dans capture.jpg")

if __name__ == "__main__":
    main()