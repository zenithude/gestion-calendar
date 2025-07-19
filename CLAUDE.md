# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Application de bureau multiplateforme pour la gestion quotidienne des rendez-vous personnels et professionnels, développée en Python avec CustomTkinter.

## Development Setup

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python main.py
```

## Commands

```bash
# Tests
python -m pytest                    # Tous les tests
python -m pytest -v                # Tests verbeux
python -m pytest --cov=src         # Tests avec couverture

# Tests spécifiques
python -m pytest src/tests/test_models.py
python -m pytest src/tests/test_database.py  
python -m pytest src/tests/test_services.py

# Lancer l'application
python main.py

# Build/Packaging
python build.py                     # Créer l'exécutable
python build.py --skip-tests        # Build sans tests
python build.py --create-spec       # Créer fichier .spec
```

## Architecture

### Structure du Projet
```
src/
├── models/          # Modèles de données (Category, Subcategory, Appointment)
├── services/        # Services métier (CategoryService, AppointmentService)
├── gui/            # Interface CustomTkinter (MainWindow, CalendarView, etc.)
├── database/       # Gestionnaire SQLite (DatabaseManager)
├── tests/          # Tests unitaires (TDD)
└── utils/          # Constantes et utilitaires
```

### Couches de l'Application
1. **Models**: Classes de données avec logique métier basique
2. **Database**: Couche d'accès aux données SQLite
3. **Services**: Logique métier et orchestration
4. **GUI**: Interface utilisateur CustomTkinter

### Conventions de Nommage
- **Classes**: PascalCase (ex: `AppointmentService`)
- **Méthodes/Fonctions**: camelCase (ex: `createAppointment()`)
- **Variables globales**: MAJUSCULES (ex: `DATABASE_PATH`)
- **Variables locales**: snake_case (ex: `appointment_id`)

## Important Notes

- **TDD**: Tests écrits en premier, tous les services ont une couverture de tests
- **Base de données**: SQLite locale (`calendar_data.db`)
- **Catégories par défaut**: Perso (Médical, Loisirs, Famille, Sport) et Pro (Réunion, Formation, Projet, Administratif)
- **Interface**: Moderne avec CustomTkinter, navigation fluide entre vues