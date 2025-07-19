# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet respecte le [Versioning Sémantique](https://semver.org/lang/fr/).

## [1.0.2] - 2024-07-19

### 🔒 Correctif de Sécurité

#### Sécurité
- **Pillow Security Update** : Mise à jour de Pillow 10.2.0 → 10.3.0 pour corriger une vulnérabilité de sécurité critique détectée par GitHub Dependabot
- **Dépendances sécurisées** : Projet sans alertes de sécurité

#### Validation
- ✅ 28 tests passent sans régression
- ✅ Application fonctionnelle avec nouvelle version Pillow
- ✅ Aucun impact sur les fonctionnalités GUI

---

## [1.0.1] - 2024-07-19

### 🐛 Corrections Critiques

#### Corrigé
- **Erreur Tkinter grab_set** : Correction de l'erreur "grab failed: window not viewable" lors de l'ouverture du dialogue de création/édition de rendez-vous
- **Intégration services** : Connexion complète du dialogue de rendez-vous aux services métier (création, modification, suppression fonctionnelles)
- **Gestion d'erreurs** : Amélioration de la gestion d'erreurs dans les opérations de base de données
- **Workflow complet** : Les rendez-vous peuvent maintenant être créés, modifiés et supprimés via l'interface

#### Ajouté
- **Tests GUI Logic** : 6 nouveaux tests couvrant les workflows complets de gestion des rendez-vous
- **Validation robuste** : Gestion d'erreurs améliorée dans les dialogues
- **Focus management** : Amélioration de la gestion du focus des fenêtres

#### Technique
- Total de **28 tests** (22 existants + 6 nouveaux)
- Correction de l'ordre d'initialisation dans les dialogues GUI
- Amélioration de la robustesse des composants d'interface

---

## [1.0.0] - 2024-07-19

### 🎉 Version Initiale

#### Ajouté
- **Interface graphique moderne** avec CustomTkinter
  - Fenêtre principale avec sidebar et zone de contenu
  - Navigation temporelle avec boutons précédent/suivant/aujourd'hui
  - Vue calendrier mensuelle avec indicateurs d'événements
  - Vue timeline quotidienne avec créneaux horaires
  - Dialogue de création/édition de rendez-vous complet

- **Gestion des rendez-vous**
  - Création de nouveaux rendez-vous avec titre, description, date/heure
  - Modification complète des événements existants
  - Suppression des rendez-vous
  - Validation des données et gestion d'erreurs

- **Système de catégorisation**
  - Catégories principales : Perso et Pro
  - Sous-catégories par défaut :
    - **Perso** : Médical, Loisirs, Famille, Sport
    - **Pro** : Réunion, Formation, Projet, Administratif
  - Interface de sélection avec combobox dynamiques

- **Base de données SQLite**
  - Gestionnaire de base de données avec tables optimisées
  - Schéma relationnel : Categories → Subcategories → Appointments
  - Requêtes optimisées pour les recherches par date
  - Gestion automatique des migrations et initialisation

- **Architecture robuste**
  - Pattern MVC avec séparation claire des responsabilités
  - Services métier pour la logique applicative
  - Modèles de données avec validation
  - Tests unitaires complets (22 tests, 100% de succès)

- **Fonctionnalités de navigation**
  - Navigation fluide entre années, mois, semaines
  - Sélection de date interactive dans le calendrier
  - Affichage contextuel des rendez-vous par jour
  - Raccourcis clavier (Ctrl+N, F5, Echap)

- **Packaging et distribution**
  - Script de build automatisé avec PyInstaller
  - Création d'exécutables cross-platform
  - Configuration spec personnalisée
  - Tests automatiques avant packaging

- **Documentation complète**
  - README détaillé avec instructions d'installation
  - Guide d'architecture et conventions de code
  - Documentation CLAUDE.md pour l'IA
  - Tests et exemples d'utilisation

#### Technique
- **Stack** : Python 3.8+, CustomTkinter 5.2.2, SQLite
- **Tests** : pytest avec couverture de code
- **Conventions** : PascalCase (classes), camelCase (méthodes), snake_case (variables)
- **TDD** : Développement piloté par les tests
- **Base de données** : SQLite local avec schéma normalisé

#### Fichiers de configuration
- `requirements.txt` : Dépendances Python
- `pytest.ini` : Configuration des tests
- `build.py` : Script de packaging
- `main.py` : Point d'entrée de l'application

---

## [Unreleased] - Prochaines versions

### 🔮 Fonctionnalités Planifiées

#### Version 1.1.0
- [ ] **Export/Import des données**
  - Export CSV pour tableurs
  - Export iCal pour autres calendriers
  - Import de données existantes
  
- [ ] **Notifications et rappels**
  - Notifications système
  - Rappels configurables (5min, 15min, 1h avant)
  - Sons d'alerte personnalisables

- [ ] **Recherche et filtres avancés**
  - Recherche textuelle dans tous les champs
  - Filtres par catégorie, sous-catégorie, date
  - Recherche par plage de dates
  - Sauvegarde des filtres favoris

- [ ] **Amélioration de l'interface**
  - Thème sombre/clair commutable
  - Personnalisation des couleurs de catégories
  - Amélioration de la responsive design
  - Mode plein écran

#### Version 1.2.0
- [ ] **Récurrence des événements**
  - Événements quotidiens, hebdomadaires, mensuels
  - Gestion des exceptions dans les récurrences
  - Interface intuitive pour définir les récurrences

- [ ] **Vue semaine détaillée**
  - Affichage semaine complète avec grille horaire
  - Glisser-déposer pour modifier les horaires
  - Vue compacte et vue étendue

- [ ] **Statistiques et rapports**
  - Temps passé par catégorie
  - Graphiques de répartition
  - Rapports mensuels/annuels
  - Export des statistiques

#### Version 1.3.0
- [ ] **Synchronisation et partage**
  - Synchronisation cloud (Google Drive, Dropbox)
  - Partage de calendriers entre utilisateurs
  - Gestion des permissions
  - Synchronisation bidirectionnelle

- [ ] **Fonctionnalités avancées**
  - Support multi-langues (FR/EN/ES)
  - Gestion des fuseaux horaires
  - Intégration avec calendriers externes
  - API REST pour intégrations tierces

---

## Légende des Types de Changements

- 🎉 **Ajouté** : Nouvelles fonctionnalités
- 🔧 **Modifié** : Changements de fonctionnalités existantes
- 🐛 **Corrigé** : Corrections de bugs
- 🗑️ **Supprimé** : Fonctionnalités supprimées
- 🔒 **Sécurité** : Corrections de vulnérabilités
- 📝 **Documentation** : Mise à jour de la documentation
- ⚡ **Performance** : Améliorations de performance
- 🎨 **Interface** : Améliorations visuelles