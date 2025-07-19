# 📅 Gestion Calendrier

Application de bureau multiplateforme pour la gestion quotidienne des rendez-vous personnels et professionnels.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-22%20passed-brightgreen.svg)

## ✨ Fonctionnalités

### 🎯 Gestion des Rendez-vous
- ✅ Créer de nouveaux rendez-vous avec titre, description, date et heure
- ✅ Catégorisation : **Perso** (Médical, Loisirs, Famille, Sport) et **Pro** (Réunion, Formation, Projet, Administratif)
- ✅ Sous-catégorisation personnalisable pour une organisation fine
- ✅ Modification complète des événements existants
- ✅ Suppression des rendez-vous

### 🗓️ Navigation Temporelle
- ✅ Navigation fluide entre années, mois et semaines
- ✅ Vue calendrier mensuelle avec aperçu des événements
- ✅ Vue chronologique quotidienne avec créneaux horaires
- ✅ Bouton "Aujourd'hui" pour retour rapide à la date courante

### 🎨 Interface Moderne
- ✅ Design moderne et intuitif avec CustomTkinter
- ✅ Sidebar avec contrôles de navigation et actions rapides
- ✅ Indicateurs visuels pour les jours avec rendez-vous
- ✅ Timeline détaillée avec affichage par créneaux horaires
- ✅ Dialogue d'édition complet avec validation des données

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation depuis le code source

```bash
# Cloner le dépôt
git clone <url-du-depot>
cd gestion-calendar

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Linux/macOS:
source venv/bin/activate
# Sur Windows:
venv\\Scripts\\activate

# Installer les dépendances
pip install -r requirements.txt
```

## 🎮 Utilisation

### Lancer l'application
```bash
python main.py
```

### Tests
```bash
# Exécuter tous les tests
python -m pytest

# Tests avec couverture
python -m pytest --cov=src

# Tests verbeux
python -m pytest -v
```

### Créer un exécutable
```bash
# Installer PyInstaller si pas déjà fait
pip install pyinstaller

# Créer l'exécutable
python build.py

# L'exécutable sera dans le dossier dist/
```

## 🏗️ Architecture

### Structure du Projet
```
gestion-calendar/
├── src/
│   ├── models/          # Modèles de données
│   │   ├── category.py
│   │   ├── subcategory.py
│   │   └── appointment.py
│   ├── services/        # Logique métier
│   │   ├── category_service.py
│   │   └── appointment_service.py
│   ├── database/        # Accès aux données
│   │   └── database_manager.py
│   ├── gui/            # Interface utilisateur
│   │   ├── main_window.py
│   │   ├── calendar_view.py
│   │   ├── timeline_view.py
│   │   └── appointment_dialog.py
│   ├── tests/          # Tests unitaires
│   └── utils/          # Utilitaires et constantes
├── main.py             # Point d'entrée
├── build.py           # Script de packaging
├── requirements.txt   # Dépendances
└── CLAUDE.md         # Guide pour Claude Code
```

### Architecture en Couches
1. **Models** : Classes de données avec logique métier basique
2. **Database** : Couche d'accès aux données SQLite
3. **Services** : Logique métier et orchestration
4. **GUI** : Interface utilisateur CustomTkinter

## 🧪 Tests

Le projet suit une approche **TDD (Test-Driven Development)** avec une couverture de tests complète :

- **22 tests unitaires** couvrant tous les composants critiques
- Tests des modèles de données
- Tests du gestionnaire de base de données
- Tests des services métier
- Validation des fonctionnalités CRUD

## 🛠️ Technologies Utilisées

- **Python 3.8+** : Langage principal
- **CustomTkinter** : Interface graphique moderne
- **SQLite** : Base de données locale
- **pytest** : Framework de tests
- **PyInstaller** : Packaging en exécutable
- **python-dateutil** : Gestion des dates

## 📝 Conventions de Code

- **Classes** : PascalCase (ex: `AppointmentService`)
- **Méthodes/Fonctions** : camelCase (ex: `createAppointment()`)
- **Variables globales** : MAJUSCULES (ex: `DATABASE_PATH`)
- **Variables locales** : snake_case (ex: `appointment_id`)

## 🔧 Configuration

### Base de Données
- Fichier SQLite local : `calendar_data.db`
- Création automatique au premier lancement
- Initialisation des catégories par défaut

### Catégories par Défaut
- **Perso** : Médical, Loisirs, Famille, Sport
- **Pro** : Réunion, Formation, Projet, Administratif

## 🚦 Roadmap

### Version 1.1.0 (Prochaine)
- [ ] Export/Import des données (CSV, iCal)
- [ ] Notifications et rappels
- [ ] Recherche et filtres avancés
- [ ] Thèmes sombres/clairs
- [ ] Récurrence des événements

### Version 1.2.0
- [ ] Synchronisation cloud
- [ ] Partage de calendriers
- [ ] Vue semaine détaillée
- [ ] Statistiques d'utilisation

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Écrire les tests en premier (TDD)
4. Implémenter la fonctionnalité
5. Commit les changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
6. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
7. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

Développé avec ❤️ pour une gestion efficace du temps.

---

*Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue !*