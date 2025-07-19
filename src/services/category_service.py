"""Service de gestion des catégories et sous-catégories"""

from typing import List, Optional
from src.database.database_manager import DatabaseManager
from src.models.category import Category
from src.models.subcategory import Subcategory
from src.utils.constants import DEFAULT_CATEGORIES, COLORS


class CategoryService:
    """Service pour la gestion des catégories et sous-catégories"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def initializeDefaultCategories(self):
        """Initialise les catégories et sous-catégories par défaut"""
        existing_categories = self.getAllCategories()
        existing_names = [cat.name for cat in existing_categories]
        
        for category_name, subcategories in DEFAULT_CATEGORIES.items():
            if category_name not in existing_names:
                color = COLORS.get(category_name, COLORS["default"])
                category_id = self.createCategory(category_name, color)
                
                # Créer les sous-catégories par défaut
                for subcategory_name in subcategories:
                    self.createSubcategory(subcategory_name, category_id, color)
    
    def createCategory(self, name: str, color: str) -> int:
        """Crée une nouvelle catégorie"""
        category = Category(name=name, color=color)
        return self.db_manager.insertCategory(category)
    
    def getAllCategories(self) -> List[Category]:
        """Récupère toutes les catégories"""
        return self.db_manager.getAllCategories()
    
    def getCategoryById(self, category_id: int) -> Optional[Category]:
        """Récupère une catégorie par son ID"""
        return self.db_manager.getCategoryById(category_id)
    
    def createSubcategory(self, name: str, category_id: int, color: str) -> int:
        """Crée une nouvelle sous-catégorie"""
        subcategory = Subcategory(name=name, category_id=category_id, color=color)
        return self.db_manager.insertSubcategory(subcategory)
    
    def getSubcategoriesByCategory(self, category_id: int) -> List[Subcategory]:
        """Récupère toutes les sous-catégories d'une catégorie"""
        return self.db_manager.getSubcategoriesByCategory(category_id)
    
    def getAllSubcategories(self) -> List[Subcategory]:
        """Récupère toutes les sous-catégories"""
        categories = self.getAllCategories()
        all_subcategories = []
        
        for category in categories:
            subcategories = self.getSubcategoriesByCategory(category.id)
            all_subcategories.extend(subcategories)
        
        return all_subcategories