"""Modèle pour les catégories d'événements"""

from typing import Optional


class Category:
    """Représente une catégorie d'événements (Perso/Pro)"""
    
    def __init__(self, id: Optional[int] = None, name: str = "", color: str = ""):
        self.id = id
        self.name = name
        self.color = color
    
    def __str__(self) -> str:
        return f"Category(id={self.id}, name='{self.name}', color='{self.color}')"
    
    def __repr__(self) -> str:
        return self.__str__()