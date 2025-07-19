"""Tests pour les modèles de données"""

import pytest
from datetime import datetime, date, time
from src.models.category import Category
from src.models.subcategory import Subcategory  
from src.models.appointment import Appointment


class TestCategory:
    
    def test_createCategory_withValidData_shouldCreateCategory(self):
        category = Category(1, "Perso", "#3B82F6")
        
        assert category.id == 1
        assert category.name == "Perso"
        assert category.color == "#3B82F6"
    
    def test_createCategory_withoutId_shouldCreateCategory(self):
        category = Category(name="Pro", color="#EF4444")
        
        assert category.id is None
        assert category.name == "Pro"
        assert category.color == "#EF4444"


class TestSubcategory:
    
    def test_createSubcategory_withValidData_shouldCreateSubcategory(self):
        subcategory = Subcategory(1, "Médical", 1, "#10B981")
        
        assert subcategory.id == 1
        assert subcategory.name == "Médical"
        assert subcategory.category_id == 1
        assert subcategory.color == "#10B981"


class TestAppointment:
    
    def test_createAppointment_withValidData_shouldCreateAppointment(self):
        start_datetime = datetime(2024, 1, 15, 10, 30)
        end_datetime = datetime(2024, 1, 15, 11, 30)
        
        appointment = Appointment(
            id=1,
            title="Rendez-vous médecin",
            description="Consultation générale",
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            category_id=1,
            subcategory_id=1
        )
        
        assert appointment.id == 1
        assert appointment.title == "Rendez-vous médecin"
        assert appointment.description == "Consultation générale"
        assert appointment.start_datetime == start_datetime
        assert appointment.end_datetime == end_datetime
        assert appointment.category_id == 1
        assert appointment.subcategory_id == 1
    
    def test_appointmentDuration_shouldReturnCorrectDuration(self):
        start_datetime = datetime(2024, 1, 15, 10, 30)
        end_datetime = datetime(2024, 1, 15, 11, 30)
        
        appointment = Appointment(
            title="Test",
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            category_id=1
        )
        
        duration = appointment.getDuration()
        assert duration.total_seconds() == 3600  # 1 heure
    
    def test_isOnDate_withCorrectDate_shouldReturnTrue(self):
        appointment_date = datetime(2024, 1, 15, 10, 30)
        
        appointment = Appointment(
            title="Test",
            start_datetime=appointment_date,
            end_datetime=appointment_date,
            category_id=1
        )
        
        assert appointment.isOnDate(date(2024, 1, 15)) is True
        assert appointment.isOnDate(date(2024, 1, 16)) is False