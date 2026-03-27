import cv2
import easyocr
import re
from config import LANGUES_OCR, CAMERA_INDEX

reader = easyocr.Reader(LANGUES_OCR, gpu=False)

def identifier_type_matricule(matricule):
    """
    Identifie le type de matricule tunisien
    """
    if not matricule:
        return "Inconnu"
    
    # Extraction des chiffres
    chiffres = re.findall(r"\d+", matricule)
    
    if not chiffres:
        return "Inconnu"
    
    # Analyse du format
    premier_groupe = chiffres[0] if len(chiffres) > 0 else ""
    
    # Taxi: نت (NT)
    if "نت" in matricule or "NT" in matricule.upper():
        return "Taxi"
    
    # Transport: séries commençant par 7, 8, 9
    if premier_groupe and len(premier_groupe) >= 1 and premier_groupe[0] in ['7', '8', '9']:
        return "Transport"
    
    # Véhicule de location: séries RS
    if "RS" in matricule.upper():
        return "Location"
    
    # Véhicule gouvernemental
    if re.search(r"\b[1-9]\s*RS\b", matricule.upper()):
        return "Gouvernemental"
    
    # Véhicule particulier: format XXX تونس YYYY
    if "تونس" in matricule or "TU" in matricule.upper():
        return "Véhicule Particulier"
    
    return "Véhicule Particulier"

def extraire_matricule_camera():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la caméra")
        return None, None
    
    print("📷 Caméra activée")
    print("👉 Appuyer sur 'S' pour capturer la plaque")
    print("👉 Appuyer sur 'Q' pour quitter")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Impossible de lire la caméra")
            break
        
        cv2.imshow("Camera - Detection Matricule", frame)
        
        key = cv2.waitKey(1)
        
        if key == ord('s'):
            cv2.imwrite("capture.jpg", frame)
            print("💾 Image capturée : capture.jpg")
            cap.release()
            cv2.destroyAllWindows()
            
            afficher_ocr(frame)
            matricule = traiter_image(frame)
            
           
        
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return None, None

def traiter_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    
    resultats = reader.readtext(thresh, detail=0)
    texte = "".join(resultats)
    
    return formatter_matricule_tunisienne(texte)

def formatter_matricule_tunisienne(texte):
    if not texte:
        return None
    
    texte = texte.replace(" ", "").replace("-", "").replace("ـ", "").upper()
    
# Fo    rmat 1 : 236 تونس 2203
    match1 = re.search(r"(\d{1,3})[Tت]?ونس(\d{1,4})", texte)
    if match1:
        return f"{match1.group(1)} تونس {match1.group(2)}"
    
    # Format 2 : 123456 نت
    match2 = re.search(r"(\d{6})نت", texte)
    if match2:
        return f"{match2.group(1)} نت"
    
    # Format 3 : 12_345678
    match3 = re.search(r"(\d{2})_(\d{6})", texte)
    if match3:
        return f"{match3.group(1)}_{match3.group(2)}"
    
    # 7 chiffres collés
    if re.match(r"^\d{7}$", texte):
        return f"{texte[:3]} تونس {texte[3:]}"
    
    return None

def afficher_ocr(image):
    try:
        results = reader.readtext(image)
        for (bbox, text, prob) in results:
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))
            
            cv2.rectangle(image, top_left, bottom_right, (0,255,0), 2)
            cv2.putText(image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        
        cv2.imshow("OCR Detection", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print("⚠️ Erreur affichage OCR :", e)