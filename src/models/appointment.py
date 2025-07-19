"""Modèle pour les rendez-vous"""

from datetime import datetime, date, timedelta
from typing import Optional


class Appointment:
    """Représente un rendez-vous dans le calendrier"""
    
    def __init__(self, id: Optional[int] = None, title: str = "", 
                 description: str = "", start_datetime: Optional[datetime] = None,
                 end_datetime: Optional[datetime] = None, category_id: Optional[int] = None,
                 subcategory_id: Optional[int] = None):
        self.id = id
        self.title = title
        self.description = description
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.category_id = category_id
        self.subcategory_id = subcategory_id
    
    def getDuration(self) -> timedelta:
        """Retourne la durée du rendez-vous"""
        if self.start_datetime and self.end_datetime:
            return self.end_datetime - self.start_datetime
        return timedelta(0)
    
    def isOnDate(self, target_date: date) -> bool:
        """Vérifie si le rendez-vous a lieu à une date donnée"""
        if self.start_datetime:
            return self.start_datetime.date() == target_date
        return False
    
    def __str__(self) -> str:
        return f"Appointment(id={self.id}, title='{self.title}', start={self.start_datetime})"
    
    def __repr__(self) -> str:
        return self.__str__()