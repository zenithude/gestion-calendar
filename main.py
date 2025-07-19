#!/usr/bin/env python3
"""
Point d'entrée principal de l'application Gestion Calendrier
"""

import sys
import os

# Ajouter le répertoire src au path Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui.main_window import MainWindow
from src.database.database_manager import DatabaseManager
from src.services.category_service import CategoryService
from src.services.appointment_service import AppointmentService


def main():
    """Fonction principale de l'application"""
    try:
        # Initialiser la base de données
        db_manager = DatabaseManager()
        db_manager.initializeDatabase()
        
        # Initialiser les services
        category_service = CategoryService(db_manager)
        appointment_service = AppointmentService(db_manager)
        
        # Initialiser les catégories par défaut
        category_service.initializeDefaultCategories()
        
        # Lancer l'interface graphique
        app = MainWindow(category_service, appointment_service)
        app.run()
        
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application: {e}")
        sys.exit(1)
    finally:
        # Fermer la connexion à la base de données
        if 'db_manager' in locals():
            db_manager.close()


if __name__ == "__main__":
    main()