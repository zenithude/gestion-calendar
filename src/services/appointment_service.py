"""Service de gestion des rendez-vous"""

from typing import List, Optional
from datetime import datetime, date, timedelta
from src.database.database_manager import DatabaseManager
from src.models.appointment import Appointment


class AppointmentService:
    """Service pour la gestion des rendez-vous"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def createAppointment(self, title: str, description: str = "", 
                         start_datetime: datetime = None, end_datetime: datetime = None,
                         category_id: int = None, subcategory_id: Optional[int] = None) -> int:
        """Crée un nouveau rendez-vous"""
        appointment = Appointment(
            title=title,
            description=description,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            category_id=category_id,
            subcategory_id=subcategory_id
        )
        return self.db_manager.insertAppointment(appointment)
    
    def getAppointmentById(self, appointment_id: int) -> Optional[Appointment]:
        """Récupère un rendez-vous par son ID"""
        # Note: Cette méthode nécessiterait d'être ajoutée au DatabaseManager
        # Pour l'instant, on utilise une approche alternative
        pass
    
    def getAppointmentsByDate(self, target_date: date) -> List[Appointment]:
        """Récupère tous les rendez-vous d'une date donnée"""
        return self.db_manager.getAppointmentsByDate(target_date)
    
    def getAppointmentsByDateRange(self, start_date: date, end_date: date) -> List[Appointment]:
        """Récupère tous les rendez-vous dans une plage de dates"""
        appointments = []
        current_date = start_date
        
        while current_date <= end_date:
            daily_appointments = self.getAppointmentsByDate(current_date)
            appointments.extend(daily_appointments)
            current_date += timedelta(days=1)
        
        # Trier par date/heure de début
        appointments.sort(key=lambda apt: apt.start_datetime)
        return appointments
    
    def updateAppointment(self, appointment_id: int, title: str = None, 
                         description: str = None, start_datetime: datetime = None,
                         end_datetime: datetime = None, category_id: int = None,
                         subcategory_id: Optional[int] = None) -> bool:
        """Met à jour un rendez-vous existant"""
        # Créer un objet appointment avec les nouvelles valeurs
        appointment = Appointment(
            id=appointment_id,
            title=title,
            description=description,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            category_id=category_id,
            subcategory_id=subcategory_id
        )
        
        return self.db_manager.updateAppointment(appointment)
    
    def deleteAppointment(self, appointment_id: int) -> bool:
        """Supprime un rendez-vous"""
        return self.db_manager.deleteAppointment(appointment_id)
    
    def getAppointmentsByCategory(self, category_id: int) -> List[Appointment]:
        """Récupère tous les rendez-vous d'une catégorie"""
        # Cette méthode nécessiterait une nouvelle requête dans DatabaseManager
        # Pour l'instant, on peut filtrer manuellement ou l'implémenter plus tard
        pass
    
    def getAppointmentsBySubcategory(self, subcategory_id: int) -> List[Appointment]:
        """Récupère tous les rendez-vous d'une sous-catégorie"""
        # Cette méthode nécessiterait une nouvelle requête dans DatabaseManager
        # Pour l'instant, on peut filtrer manuellement ou l'implémenter plus tard
        pass
    
    def getUpcomingAppointments(self, days_ahead: int = 7) -> List[Appointment]:
        """Récupère les rendez-vous à venir dans les N prochains jours"""
        today = date.today()
        end_date = today + timedelta(days=days_ahead)
        
        return self.getAppointmentsByDateRange(today, end_date)
    
    def hasConflict(self, start_datetime: datetime, end_datetime: datetime, 
                   exclude_id: Optional[int] = None) -> bool:
        """Vérifie s'il y a un conflit d'horaire avec un autre rendez-vous"""
        target_date = start_datetime.date()
        existing_appointments = self.getAppointmentsByDate(target_date)
        
        for appointment in existing_appointments:
            # Exclure le rendez-vous en cours de modification
            if exclude_id and appointment.id == exclude_id:
                continue
            
            # Vérifier les chevauchements
            if (start_datetime < appointment.end_datetime and 
                end_datetime > appointment.start_datetime):
                return True
        
        return False