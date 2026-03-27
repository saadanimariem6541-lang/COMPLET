"""
Script principal pour lancer le système complet
"""
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def start_backend():
    """Démarre le serveur backend Flask"""
    print("🚀 Démarrage du serveur backend...")
    backend_process = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)  # Attendre que le serveur démarre
    print("✅ Backend démarré sur http://127.0.0.1:5000")
    return backend_process

def open_dashboard():
    """Ouvre le dashboard dans le navigateur"""
    dashboard_path = Path("frontend/dashboard_no_logo.html").absolute()
    print(f"🌐 Ouverture du dashboard...")
    webbrowser.open(f"file:///{dashboard_path}")
    print("✅ Dashboard ouvert dans le navigateur")

def main():
    print("=" * 60)
    print("🚦 SYSTÈME DE GESTION D'ACCÈS VÉHICULES")
    print("=" * 60)
    
    # Démarrer le backend
    backend = start_backend()
    
    # Ouvrir le dashboard
    time.sleep(1)
    open_dashboard()
    
    print("\n" + "=" * 60)
    print("📋 INSTRUCTIONS:")
    print("=" * 60)
    print("1. Le dashboard est ouvert dans votre navigateur")
    print("2. Pour capturer une plaque, exécutez: python main.py")
    print("3. Les données apparaîtront automatiquement dans le dashboard")
    print("4. Appuyez sur Ctrl+C pour arrêter le serveur")
    print("=" * 60)
    
    try:
        # Garder le serveur actif
        backend.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt du système...")
        backend.terminate()
        print("✅ Système arrêté")

if __name__ == "__main__":
    main()