"""Tests pour les services métier"""

import pytest
import tempfile
import os
from datetime import datetime, date
from src.services.appointment_service import AppointmentService
from src.services.category_service import CategoryService
from src.database.database_manager import DatabaseManager
from src.models.category import Category
from src.models.subcategory import Subcategory
from src.models.appointment import Appointment


class TestCategoryService:
    
    @pytest.fixture
    def category_service(self):
        """Crée un service de catégorie avec une base temporaire"""
        temp_fd, temp_path = tempfile.mkstemp(suffix=".db")
        os.close(temp_fd)
        db_manager = DatabaseManager(temp_path)
        db_manager.initializeDatabase()
        service = CategoryService(db_manager)
        yield service
        os.unlink(temp_path)
    
    def test_initializeDefaultCategories_shouldCreateDefaultCategories(self, category_service):
        """Test de l'initialisation des catégories par défaut"""
        category_service.initializeDefaultCategories()
        
        categories = category_service.getAllCategories()
        category_names = [cat.name for cat in categories]
        
        assert "Perso" in category_names
        assert "Pro" in category_names
    
    def test_createCategory_withValidData_shouldReturnCategoryId(self, category_service):
        """Test de création d'une catégorie"""
        category_id = category_service.createCategory("Test", "#FF5722")
        
        assert category_id is not None
        assert category_id > 0
    
    def test_createSubcategory_withValidData_shouldReturnSubcategoryId(self, category_service):
        """Test de création d'une sous-catégorie"""
        # Créer une catégorie parent
        category_id = category_service.createCategory("Perso", "#3B82F6")
        
        # Créer une sous-catégorie
        subcategory_id = category_service.createSubcategory("Sport", category_id, "#10B981")
        
        assert subcategory_id is not None
        assert subcategory_id > 0
    
    def test_getSubcategoriesByCategory_shouldReturnFilteredSubcategories(self, category_service):
        """Test de récupération des sous-catégories par catégorie"""
        # Créer des catégories
        perso_id = category_service.createCategory("Perso", "#3B82F6")
        pro_id = category_service.createCategory("Pro", "#EF4444")
        
        # Créer des sous-catégories
        category_service.createSubcategory("Sport", perso_id, "#10B981")
        category_service.createSubcategory("Médical", perso_id, "#F59E0B")
        category_service.createSubcategory("Réunion", pro_id, "#8B5CF6")
        
        # Récupérer les sous-catégories Perso
        perso_subcategories = category_service.getSubcategoriesByCategory(perso_id)
        
        assert len(perso_subcategories) == 2
        subcategory_names = [sub.name for sub in perso_subcategories]
        assert "Sport" in subcategory_names
        assert "Médical" in subcategory_names


class TestAppointmentService:
    
    @pytest.fixture
    def appointment_service(self):
        """Crée un service de rendez-vous avec une base temporaire"""
        temp_fd, temp_path = tempfile.mkstemp(suffix=".db")
        os.close(temp_fd)
        db_manager = DatabaseManager(temp_path)
        db_manager.initializeDatabase()
        service = AppointmentService(db_manager)
        yield service
        os.unlink(temp_path)
    
    @pytest.fixture
    def sample_category_id(self, appointment_service):
        """Crée une catégorie de test"""
        category = Category(name="Test", color="#3B82F6")
        return appointment_service.db_manager.insertCategory(category)
    
    def test_createAppointment_withValidData_shouldReturnAppointmentId(self, appointment_service, sample_category_id):
        """Test de création d'un rendez-vous"""
        appointment_id = appointment_service.createAppointment(
            title="Rendez-vous test",
            description="Description test",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=sample_category_id
        )
        
        assert appointment_id is not None
        assert appointment_id > 0
    
    def test_getAppointmentsByDate_shouldReturnFilteredAppointments(self, appointment_service, sample_category_id):
        """Test de récupération des rendez-vous par date"""
        # Créer plusieurs rendez-vous
        appointment_service.createAppointment(
            title="RDV 1",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=sample_category_id
        )
        appointment_service.createAppointment(
            title="RDV 2",
            start_datetime=datetime(2024, 1, 16, 14, 0),
            end_datetime=datetime(2024, 1, 16, 15, 0),
            category_id=sample_category_id
        )
        
        # Récupérer les rendez-vous du 15 janvier
        appointments = appointment_service.getAppointmentsByDate(date(2024, 1, 15))
        
        assert len(appointments) == 1
        assert appointments[0].title == "RDV 1"
    
    def test_updateAppointment_shouldModifyExistingAppointment(self, appointment_service, sample_category_id):
        """Test de modification d'un rendez-vous"""
        # Créer un rendez-vous
        appointment_id = appointment_service.createAppointment(
            title="RDV Original",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=sample_category_id
        )
        
        # Modifier le rendez-vous
        success = appointment_service.updateAppointment(
            appointment_id=appointment_id,
            title="RDV Modifié",
            description="Nouvelle description",
            start_datetime=datetime(2024, 1, 15, 14, 0),
            end_datetime=datetime(2024, 1, 15, 15, 0),
            category_id=sample_category_id
        )
        
        assert success is True
        
        # Vérifier la modification
        appointments = appointment_service.getAppointmentsByDate(date(2024, 1, 15))
        assert len(appointments) == 1
        assert appointments[0].title == "RDV Modifié"
        assert appointments[0].start_datetime.hour == 14
    
    def test_deleteAppointment_shouldRemoveAppointment(self, appointment_service, sample_category_id):
        """Test de suppression d'un rendez-vous"""
        # Créer un rendez-vous
        appointment_id = appointment_service.createAppointment(
            title="RDV à supprimer",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=sample_category_id
        )
        
        # Supprimer le rendez-vous
        success = appointment_service.deleteAppointment(appointment_id)
        
        assert success is True
        
        # Vérifier la suppression
        appointments = appointment_service.getAppointmentsByDate(date(2024, 1, 15))
        assert len(appointments) == 0
    
    def test_getAppointmentsByDateRange_shouldReturnFilteredAppointments(self, appointment_service, sample_category_id):
        """Test de récupération des rendez-vous par plage de dates"""
        # Créer plusieurs rendez-vous
        appointment_service.createAppointment(
            title="RDV 1",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=sample_category_id
        )
        appointment_service.createAppointment(
            title="RDV 2",
            start_datetime=datetime(2024, 1, 17, 14, 0),
            end_datetime=datetime(2024, 1, 17, 15, 0),
            category_id=sample_category_id
        )
        appointment_service.createAppointment(
            title="RDV 3",
            start_datetime=datetime(2024, 1, 20, 9, 0),
            end_datetime=datetime(2024, 1, 20, 10, 0),
            category_id=sample_category_id
        )
        
        # Récupérer les rendez-vous entre le 16 et 18 janvier
        appointments = appointment_service.getAppointmentsByDateRange(
            start_date=date(2024, 1, 16),
            end_date=date(2024, 1, 18)
        )
        
        assert len(appointments) == 1
        assert appointments[0].title == "RDV 2"