"""
Script de test pour vérifier la détection de type de matricule
"""
from ocr import identifier_type_matricule, formatter_matricule_tunisienne
from database import init_db, enregistrer_acces
from datetime import datetime

def test_types_matricules():
    print("🧪 Test de détection des types de matricules")
    print("=" * 60)
    
    # Exemples de matricules tunisiennes
    test_cases = [
        ("236 تونس 2203"),
        ("123456 نت"),
        ("789 تونس 1234"),
        ("456 تونس 5678"),
        ("234567 نت"),
        ("912 تونس 3456"),
    ]
    
    print("\n📋 Tests de détection:\n")
    
    for matricule, expected_type in test_cases:
        detected_type = identifier_type_matricule(matricule)
        status = "✅" if detected_type == expected_type else "⚠️"
        print(f"{status} Matricule: {matricule}")
    
        print()

def test_database_integration():
    print("\n💾 Test d'intégration avec la base de données")
    print("=" * 60)
    
    # Initialiser la base de données
    init_db()
    print("✅ Base de données initialisée")
    
    # Tester l'enregistrement
    test_matricules = [
        ("236 تونس 2203"),
        ("123456 نت"),
        ("789 تونس 1234"),
    ]
    
    for matricule in test_matricules:
        date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        statut = "AUTORISÉ"
        
        try:
            enregistrer_acces(matricule, date_heure, statut)
            print(f"✅ Enregistré: {matricule}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    print("\n✅ Test d'intégration terminé!")

def test_formatter():
    print("\n🔧 Test du formateur de matricules")
    print("=" * 60)
    
    test_inputs = [
        "236تونس2203",
        "123456نت",
        "7891234",
    ]
    
    for input_text in test_inputs:
        result = formatter_matricule_tunisienne(input_text)
        print(f"Input:  {input_text}")
        print(f"Output: {result}")
        

if __name__ == "__main__":
    print("\n🚀 Démarrage des tests du système\n")
    
    # Test 1: Types de matricules
    test_types_matricules()
    
    # Test 2: Formateur
    test_formatter()
    
    # Test 3: Base de données
    test_database_integration()
    
    print("\n" + "=" * 60)
    print("✅ Tous les tests sont terminés!")
    print("=" * 60)