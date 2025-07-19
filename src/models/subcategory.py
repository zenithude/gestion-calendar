"""Modèle pour les sous-catégories d'événements"""

from typing import Optional


class Subcategory:
    """Représente une sous-catégorie d'événements"""
    
    def __init__(self, id: Optional[int] = None, name: str = "", 
                 category_id: Optional[int] = None, color: str = ""):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.color = color
    
    def __str__(self) -> str:
        return f"Subcategory(id={self.id}, name='{self.name}', category_id={self.category_id}, color='{self.color}')"
    
    def __repr__(self) -> str:
        return self.__str__()