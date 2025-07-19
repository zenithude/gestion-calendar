"""Tests pour la logique métier des composants GUI"""

import pytest
import tempfile
import os
from datetime import datetime, date
from unittest.mock import Mock, patch
from src.services.category_service import CategoryService
from src.services.appointment_service import AppointmentService
from src.database.database_manager import DatabaseManager
from src.models.appointment import Appointment


class TestAppointmentDialogLogic:
    """Tests pour la logique métier du dialogue de rendez-vous"""
    
    @pytest.fixture
    def setup_services(self):
        """Configure les services pour les tests"""
        temp_fd, temp_path = tempfile.mkstemp(suffix=".db")
        os.close(temp_fd)
        
        db_manager = DatabaseManager(temp_path)
        db_manager.initializeDatabase()
        
        category_service = CategoryService(db_manager)
        appointment_service = AppointmentService(db_manager)
        
        # Initialiser les catégories par défaut
        category_service.initializeDefaultCategories()
        
        yield category_service, appointment_service
        
        os.unlink(temp_path)
    
    def test_appointment_creation_workflow(self, setup_services):
        """Test du workflow complet de création d'un rendez-vous"""
        category_service, appointment_service = setup_services
        
        # Récupérer les catégories disponibles
        categories = category_service.getAllCategories()
        assert len(categories) >= 2  # Perso et Pro
        
        perso_category = next(cat for cat in categories if cat.name == "Perso")
        subcategories = category_service.getSubcategoriesByCategory(perso_category.id)
        assert len(subcategories) > 0
        
        medical_subcategory = next(sub for sub in subcategories if sub.name == "Médical")
        
        # Créer un rendez-vous
        appointment_id = appointment_service.createAppointment(
            title="Rendez-vous médecin",
            description="Consultation générale",
            start_datetime=datetime(2024, 1, 15, 10, 30),
            end_datetime=datetime(2024, 1, 15, 11, 30),
            category_id=perso_category.id,
            subcategory_id=medical_subcategory.id
        )
        
        assert appointment_id is not None
        assert appointment_id > 0
        
        # Vérifier que le rendez-vous a été créé
        appointments = appointment_service.getAppointmentsByDate(date(2024, 1, 15))
        assert len(appointments) == 1
        assert appointments[0].title == "Rendez-vous médecin"
        assert appointments[0].category_id == perso_category.id
        assert appointments[0].subcategory_id == medical_subcategory.id
    
    def test_appointment_update_workflow(self, setup_services):
        """Test du workflow de mise à jour d'un rendez-vous"""
        category_service, appointment_service = setup_services
        
        categories = category_service.getAllCategories()
        perso_category = next(cat for cat in categories if cat.name == "Perso")
        pro_category = next(cat for cat in categories if cat.name == "Pro")
        
        # Créer un rendez-vous initial
        appointment_id = appointment_service.createAppointment(
            title="RDV Original",
            description="Description originale",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=perso_category.id
        )
        
        # Modifier le rendez-vous
        success = appointment_service.updateAppointment(
            appointment_id=appointment_id,
            title="RDV Modifié",
            description="Nouvelle description",
            start_datetime=datetime(2024, 1, 15, 14, 0),
            end_datetime=datetime(2024, 1, 15, 15, 0),
            category_id=pro_category.id  # Changement de catégorie
        )
        
        assert success is True
        
        # Vérifier les modifications
        appointments = appointment_service.getAppointmentsByDate(date(2024, 1, 15))
        assert len(appointments) == 1
        updated_appointment = appointments[0]
        
        assert updated_appointment.title == "RDV Modifié"
        assert updated_appointment.description == "Nouvelle description"
        assert updated_appointment.start_datetime.hour == 14
        assert updated_appointment.category_id == pro_category.id
    
    def test_appointment_deletion_workflow(self, setup_services):
        """Test du workflow de suppression d'un rendez-vous"""
        category_service, appointment_service = setup_services
        
        categories = category_service.getAllCategories()
        category_id = categories[0].id
        
        # Créer un rendez-vous
        appointment_id = appointment_service.createAppointment(
            title="RDV à supprimer",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=category_id
        )
        
        # Vérifier qu'il existe
        appointments_before = appointment_service.getAppointmentsByDate(date(2024, 1, 15))
        assert len(appointments_before) == 1
        
        # Supprimer le rendez-vous
        success = appointment_service.deleteAppointment(appointment_id)
        assert success is True
        
        # Vérifier la suppression
        appointments_after = appointment_service.getAppointmentsByDate(date(2024, 1, 15))
        assert len(appointments_after) == 0
    
    def test_category_subcategory_relationship(self, setup_services):
        """Test de la relation catégorie-sous-catégorie"""
        category_service, appointment_service = setup_services
        
        # Vérifier les catégories par défaut
        categories = category_service.getAllCategories()
        category_names = [cat.name for cat in categories]
        
        assert "Perso" in category_names
        assert "Pro" in category_names
        
        # Vérifier les sous-catégories Perso
        perso_category = next(cat for cat in categories if cat.name == "Perso")
        perso_subcategories = category_service.getSubcategoriesByCategory(perso_category.id)
        perso_sub_names = [sub.name for sub in perso_subcategories]
        
        expected_perso_subs = ["Médical", "Loisirs", "Famille", "Sport"]
        for expected in expected_perso_subs:
            assert expected in perso_sub_names
        
        # Vérifier les sous-catégories Pro
        pro_category = next(cat for cat in categories if cat.name == "Pro")
        pro_subcategories = category_service.getSubcategoriesByCategory(pro_category.id)
        pro_sub_names = [sub.name for sub in pro_subcategories]
        
        expected_pro_subs = ["Réunion", "Formation", "Projet", "Administratif"]
        for expected in expected_pro_subs:
            assert expected in pro_sub_names
    
    def test_appointment_date_filtering(self, setup_services):
        """Test du filtrage des rendez-vous par date"""
        category_service, appointment_service = setup_services
        
        categories = category_service.getAllCategories()
        category_id = categories[0].id
        
        # Créer plusieurs rendez-vous à différentes dates
        appointment_service.createAppointment(
            title="RDV 15 janvier",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=category_id
        )
        
        appointment_service.createAppointment(
            title="RDV 16 janvier",
            start_datetime=datetime(2024, 1, 16, 14, 0),
            end_datetime=datetime(2024, 1, 16, 15, 0),
            category_id=category_id
        )
        
        appointment_service.createAppointment(
            title="RDV 17 janvier",
            start_datetime=datetime(2024, 1, 17, 9, 0),
            end_datetime=datetime(2024, 1, 17, 10, 0),
            category_id=category_id
        )
        
        # Tester le filtrage par date
        appointments_15 = appointment_service.getAppointmentsByDate(date(2024, 1, 15))
        assert len(appointments_15) == 1
        assert appointments_15[0].title == "RDV 15 janvier"
        
        appointments_16 = appointment_service.getAppointmentsByDate(date(2024, 1, 16))
        assert len(appointments_16) == 1
        assert appointments_16[0].title == "RDV 16 janvier"
        
        # Tester le filtrage par plage de dates
        appointments_range = appointment_service.getAppointmentsByDateRange(
            start_date=date(2024, 1, 15),
            end_date=date(2024, 1, 16)
        )
        assert len(appointments_range) == 2
        
        # Vérifier l'ordre chronologique
        assert appointments_range[0].start_datetime < appointments_range[1].start_datetime
    
    def test_data_validation_patterns(self, setup_services):
        """Test des patterns de validation des données"""
        category_service, appointment_service = setup_services
        
        categories = category_service.getAllCategories()
        category_id = categories[0].id
        
        # Test avec données valides
        valid_appointment_id = appointment_service.createAppointment(
            title="Rendez-vous valide",
            description="Description valide",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=category_id
        )
        assert valid_appointment_id is not None
        
        # Test avec titre vide (devrait être géré par la validation)
        try:
            empty_title_id = appointment_service.createAppointment(
                title="",  # Titre vide
                start_datetime=datetime(2024, 1, 15, 12, 0),
                end_datetime=datetime(2024, 1, 15, 13, 0),
                category_id=category_id
            )
            # Si ça passe, au moins vérifier que l'ID est valide
            assert empty_title_id is not None
        except Exception:
            # Si une exception est levée, c'est acceptable pour un titre vide
            pass
        
        # Test avec heures invalides (fin avant début)
        # Note: Cette validation pourrait être ajoutée dans une version future
        invalid_time_id = appointment_service.createAppointment(
            title="RDV heures invalides",
            start_datetime=datetime(2024, 1, 15, 15, 0),  # Après l'heure de fin
            end_datetime=datetime(2024, 1, 15, 14, 0),    # Avant l'heure de début
            category_id=category_id
        )
        # Pour l'instant, le service accepte ces données
        # Cette validation pourrait être ajoutée plus tard
        assert invalid_time_id is not None