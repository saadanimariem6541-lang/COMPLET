"""
Script pour ajouter un enregistrement test
"""
from database import init_db, enregistrer_acces
from datetime import datetime

# Initialiser la base de données
init_db()

# Ajouter un enregistrement test
matricule = "236 تونس 2203"
type_vehicule = "Véhicule Particulier"
date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
statut = "AUTORISÉ"

enregistrer_acces(matricule, date_heure, statut)
print(f"✅ Enregistrement ajouté:")
print(f"   Matricule: {matricule}")
print(f"   Date: {date_heure}")
print(f"   Statut: {statut}")
print("\n🌐 Vérifiez le dashboard maintenant!")