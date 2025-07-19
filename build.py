#!/usr/bin/env python3
"""
Script de packaging pour créer l'exécutable de l'application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_application():
    """Construit l'application avec PyInstaller"""
    
    print("🏗️  Construction de l'application Gestion Calendrier...")
    
    # Chemins
    project_root = Path(__file__).parent
    main_file = project_root / "main.py"
    build_dir = project_root / "build"
    dist_dir = project_root / "dist"
    
    # Nettoyer les dossiers de build précédents
    if build_dir.exists():
        print("🧹 Nettoyage du dossier build...")
        shutil.rmtree(build_dir)
    
    if dist_dir.exists():
        print("🧹 Nettoyage du dossier dist...")
        shutil.rmtree(dist_dir)
    
    # Options PyInstaller
    pyinstaller_args = [
        "pyinstaller",
        "--name=GestionCalendrier",
        "--onefile",                    # Un seul fichier exécutable
        "--windowed",                   # Pas de console (GUI uniquement)
        "--add-data=src:src",          # Inclure le dossier src
        "--hidden-import=customtkinter",
        "--hidden-import=PIL",
        "--hidden-import=sqlite3",
        "--clean",                      # Nettoyer avant construction
        str(main_file)
    ]
    
    # Ajouter une icône si disponible
    icon_path = project_root / "assets" / "icon.ico"
    if icon_path.exists():
        pyinstaller_args.extend(["--icon", str(icon_path)])
    
    print(f"📦 Exécution de PyInstaller...")
    print(f"Commande: {' '.join(pyinstaller_args)}")
    
    try:
        # Exécuter PyInstaller
        result = subprocess.run(pyinstaller_args, check=True, capture_output=True, text=True)
        print("✅ Construction réussie!")
        
        # Afficher l'emplacement de l'exécutable
        executable_path = dist_dir / "GestionCalendrier"
        if sys.platform == "win32":
            executable_path = executable_path.with_suffix(".exe")
        
        if executable_path.exists():
            print(f"📍 Exécutable créé: {executable_path}")
            print(f"📊 Taille: {executable_path.stat().st_size / (1024*1024):.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la construction:")
        print(f"Code de retour: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def create_spec_file():
    """Crée un fichier .spec personnalisé pour PyInstaller"""
    
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('src', 'src')],
    hiddenimports=[
        'customtkinter',
        'PIL',
        'sqlite3',
        'dateutil'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GestionCalendrier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open("GestionCalendrier.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("📝 Fichier .spec créé: GestionCalendrier.spec")

def run_tests_before_build():
    """Exécute les tests avant la construction"""
    print("🧪 Exécution des tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "-v"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Tous les tests passent!")
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ Des tests échouent. Construction annulée.")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Fonction principale du script de build"""
    print("🚀 Script de build - Gestion Calendrier")
    print("=" * 50)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path("main.py").exists():
        print("❌ Erreur: main.py non trouvé. Exécutez ce script depuis la racine du projet.")
        sys.exit(1)
    
    # Optionnel: exécuter les tests d'abord
    if "--skip-tests" not in sys.argv:
        if not run_tests_before_build():
            sys.exit(1)
    
    # Créer le fichier .spec si demandé
    if "--create-spec" in sys.argv:
        create_spec_file()
        return
    
    # Construire l'application
    success = build_application()
    
    if success:
        print("\n🎉 Construction terminée avec succès!")
        print("💡 Vous pouvez maintenant distribuer l'exécutable dans le dossier 'dist/'")
    else:
        print("\n💥 Échec de la construction")
        sys.exit(1)

if __name__ == "__main__":
    main()