"""Tests pour le gestionnaire de base de données"""

import pytest
import sqlite3
import tempfile
import os
from datetime import datetime
from src.database.database_manager import DatabaseManager
from src.models.category import Category
from src.models.subcategory import Subcategory
from src.models.appointment import Appointment


class TestDatabaseManager:
    
    @pytest.fixture
    def temp_db(self):
        """Crée une base de données temporaire pour les tests"""
        temp_fd, temp_path = tempfile.mkstemp(suffix=".db")
        os.close(temp_fd)
        db_manager = DatabaseManager(temp_path)
        yield db_manager
        os.unlink(temp_path)
    
    def test_initializeDatabase_shouldCreateTables(self, temp_db):
        """Test de l'initialisation de la base de données"""
        temp_db.initializeDatabase()
        
        # Vérifier que les tables existent
        cursor = temp_db.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert "categories" in tables
        assert "subcategories" in tables
        assert "appointments" in tables
    
    def test_insertCategory_shouldReturnCategoryId(self, temp_db):
        """Test d'insertion d'une catégorie"""
        temp_db.initializeDatabase()
        
        category = Category(name="Perso", color="#3B82F6")
        category_id = temp_db.insertCategory(category)
        
        assert category_id is not None
        assert category_id > 0
    
    def test_getCategoryById_shouldReturnCategory(self, temp_db):
        """Test de récupération d'une catégorie par ID"""
        temp_db.initializeDatabase()
        
        # Insérer une catégorie
        category = Category(name="Pro", color="#EF4444")
        category_id = temp_db.insertCategory(category)
        
        # Récupérer la catégorie
        retrieved_category = temp_db.getCategoryById(category_id)
        
        assert retrieved_category is not None
        assert retrieved_category.id == category_id
        assert retrieved_category.name == "Pro"
        assert retrieved_category.color == "#EF4444"
    
    def test_getAllCategories_shouldReturnAllCategories(self, temp_db):
        """Test de récupération de toutes les catégories"""
        temp_db.initializeDatabase()
        
        # Insérer plusieurs catégories
        temp_db.insertCategory(Category(name="Perso", color="#3B82F6"))
        temp_db.insertCategory(Category(name="Pro", color="#EF4444"))
        
        categories = temp_db.getAllCategories()
        
        assert len(categories) == 2
        assert any(cat.name == "Perso" for cat in categories)
        assert any(cat.name == "Pro" for cat in categories)
    
    def test_insertSubcategory_shouldReturnSubcategoryId(self, temp_db):
        """Test d'insertion d'une sous-catégorie"""
        temp_db.initializeDatabase()
        
        # Insérer une catégorie parent
        category_id = temp_db.insertCategory(Category(name="Perso", color="#3B82F6"))
        
        # Insérer une sous-catégorie
        subcategory = Subcategory(name="Médical", category_id=category_id, color="#10B981")
        subcategory_id = temp_db.insertSubcategory(subcategory)
        
        assert subcategory_id is not None
        assert subcategory_id > 0
    
    def test_insertAppointment_shouldReturnAppointmentId(self, temp_db):
        """Test d'insertion d'un rendez-vous"""
        temp_db.initializeDatabase()
        
        # Préparer les données
        category_id = temp_db.insertCategory(Category(name="Perso", color="#3B82F6"))
        subcategory_id = temp_db.insertSubcategory(
            Subcategory(name="Médical", category_id=category_id, color="#10B981")
        )
        
        # Insérer un rendez-vous
        appointment = Appointment(
            title="Rendez-vous médecin",
            description="Consultation générale",
            start_datetime=datetime(2024, 1, 15, 10, 30),
            end_datetime=datetime(2024, 1, 15, 11, 30),
            category_id=category_id,
            subcategory_id=subcategory_id
        )
        
        appointment_id = temp_db.insertAppointment(appointment)
        
        assert appointment_id is not None
        assert appointment_id > 0
    
    def test_getAppointmentsByDate_shouldReturnFilteredAppointments(self, temp_db):
        """Test de récupération des rendez-vous par date"""
        temp_db.initializeDatabase()
        
        # Préparer les données
        category_id = temp_db.insertCategory(Category(name="Perso", color="#3B82F6"))
        
        # Insérer plusieurs rendez-vous
        appointment1 = Appointment(
            title="RDV 1",
            start_datetime=datetime(2024, 1, 15, 10, 0),
            end_datetime=datetime(2024, 1, 15, 11, 0),
            category_id=category_id
        )
        appointment2 = Appointment(
            title="RDV 2",
            start_datetime=datetime(2024, 1, 16, 14, 0),
            end_datetime=datetime(2024, 1, 16, 15, 0),
            category_id=category_id
        )
        
        temp_db.insertAppointment(appointment1)
        temp_db.insertAppointment(appointment2)
        
        # Récupérer les rendez-vous du 15 janvier
        appointments = temp_db.getAppointmentsByDate(datetime(2024, 1, 15).date())
        
        assert len(appointments) == 1
        assert appointments[0].title == "RDV 1"