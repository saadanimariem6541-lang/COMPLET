# 🚦 Système de Gestion d'Accès Véhicules

## 📋 Instructions d'utilisation

### Méthode 1: Démarrage automatique (Windows)

1. **Double-cliquez sur `start_system.bat`**
   - Le backend démarre automatiquement
   - Le dashboard s'ouvre dans votre navigateur

2. **Capturez une plaque:**
   ```bash
   python main.py
   ```
   - Appuyez sur 'S' pour capturer
   - Le matricule et le type de véhicule s'affichent automatiquement dans le dashboard

### Méthode 2: Démarrage manuel

#### Étape 1: Démarrer le backend
```bash
python backend/app.py
```
Le serveur démarre sur http://127.0.0.1:5000

#### Étape 2: Ouvrir le dashboard
Ouvrez `frontend/dashboard_no_logo.html` dans votre navigateur

#### Étape 3: Capturer des plaques
```bash
python main.py
```
- Appuyez sur 'S' pour capturer la plaque
- Appuyez sur 'Q' pour quitter

### 🎯 Fonctionnalités

✅ Détection automatique du matricule via OCR
✅ Identification du type de véhicule:
   - Véhicule Particulier (تونس)
   - Taxi (نت)
   - Transport (7xx, 8xx, 9xx)
   - Location (RS)
   - Gouvernemental

✅ Affichage en temps réel dans le dashboard
✅ Historique des accès
✅ Statistiques (Total, Autorisés, Refusés)

### 🧪 Tests

Pour tester sans caméra:
```bash
python test_ocr_type.py
```

### 📊 Base de données

Les données sont stockées dans: `database/acces.db`

Colonnes:
- matricule
- date_heure
- statut
- type_vehicule

### 🔧 Configuration

Modifiez `config.py` pour:
- Changer l'index de la caméra (CAMERA_INDEX)
- Modifier les langues OCR (LANGUES_OCR)