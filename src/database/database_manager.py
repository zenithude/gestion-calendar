"""Gestionnaire de base de données SQLite"""

import sqlite3
from typing import List, Optional
from datetime import date, datetime
from src.models.category import Category
from src.models.subcategory import Subcategory
from src.models.appointment import Appointment
from src.utils.constants import DATABASE_PATH


class DatabaseManager:
    """Gestionnaire principal pour les opérations de base de données"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.connection = None
        self.connectToDatabase()
    
    def connectToDatabase(self):
        """Établit la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise Exception(f"Erreur de connexion à la base de données: {e}")
    
    def initializeDatabase(self):
        """Initialise les tables de la base de données"""
        cursor = self.connection.cursor()
        
        # Table des catégories
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                color TEXT NOT NULL
            )
        """)
        
        # Table des sous-catégories
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subcategories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                color TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)
        
        # Table des rendez-vous
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_datetime TEXT NOT NULL,
                end_datetime TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                subcategory_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id),
                FOREIGN KEY (subcategory_id) REFERENCES subcategories (id)
            )
        """)
        
        self.connection.commit()
    
    def insertCategory(self, category: Category) -> int:
        """Insère une nouvelle catégorie et retourne son ID"""
        cursor = self.connection.cursor()
        
        cursor.execute(
            "INSERT INTO categories (name, color) VALUES (?, ?)",
            (category.name, category.color)
        )
        
        self.connection.commit()
        return cursor.lastrowid
    
    def getCategoryById(self, category_id: int) -> Optional[Category]:
        """Récupère une catégorie par son ID"""
        cursor = self.connection.cursor()
        
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        
        if row:
            return Category(
                id=row["id"],
                name=row["name"],
                color=row["color"]
            )
        return None
    
    def getAllCategories(self) -> List[Category]:
        """Récupère toutes les catégories"""
        cursor = self.connection.cursor()
        
        cursor.execute("SELECT * FROM categories ORDER BY name")
        rows = cursor.fetchall()
        
        return [
            Category(
                id=row["id"],
                name=row["name"],
                color=row["color"]
            )
            for row in rows
        ]
    
    def insertSubcategory(self, subcategory: Subcategory) -> int:
        """Insère une nouvelle sous-catégorie et retourne son ID"""
        cursor = self.connection.cursor()
        
        cursor.execute(
            "INSERT INTO subcategories (name, category_id, color) VALUES (?, ?, ?)",
            (subcategory.name, subcategory.category_id, subcategory.color)
        )
        
        self.connection.commit()
        return cursor.lastrowid
    
    def getSubcategoriesByCategory(self, category_id: int) -> List[Subcategory]:
        """Récupère toutes les sous-catégories d'une catégorie"""
        cursor = self.connection.cursor()
        
        cursor.execute(
            "SELECT * FROM subcategories WHERE category_id = ? ORDER BY name",
            (category_id,)
        )
        rows = cursor.fetchall()
        
        return [
            Subcategory(
                id=row["id"],
                name=row["name"],
                category_id=row["category_id"],
                color=row["color"]
            )
            for row in rows
        ]
    
    def insertAppointment(self, appointment: Appointment) -> int:
        """Insère un nouveau rendez-vous et retourne son ID"""
        cursor = self.connection.cursor()
        
        cursor.execute(
            """INSERT INTO appointments 
               (title, description, start_datetime, end_datetime, category_id, subcategory_id) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                appointment.title,
                appointment.description,
                appointment.start_datetime.isoformat(),
                appointment.end_datetime.isoformat(),
                appointment.category_id,
                appointment.subcategory_id
            )
        )
        
        self.connection.commit()
        return cursor.lastrowid
    
    def getAppointmentsByDate(self, target_date: date) -> List[Appointment]:
        """Récupère tous les rendez-vous d'une date donnée"""
        cursor = self.connection.cursor()
        
        # Convertir la date en format ISO pour la comparaison
        date_start = f"{target_date.strftime('%Y-%m-%d')}T00:00:00"
        date_end = f"{target_date.strftime('%Y-%m-%d')}T23:59:59"
        
        cursor.execute(
            """SELECT * FROM appointments 
               WHERE start_datetime >= ? AND start_datetime <= ?
               ORDER BY start_datetime""",
            (date_start, date_end)
        )
        rows = cursor.fetchall()
        
        return [
            Appointment(
                id=row["id"],
                title=row["title"],
                description=row["description"],
                start_datetime=datetime.fromisoformat(row["start_datetime"]),
                end_datetime=datetime.fromisoformat(row["end_datetime"]),
                category_id=row["category_id"],
                subcategory_id=row["subcategory_id"]
            )
            for row in rows
        ]
    
    def updateAppointment(self, appointment: Appointment) -> bool:
        """Met à jour un rendez-vous existant"""
        cursor = self.connection.cursor()
        
        cursor.execute(
            """UPDATE appointments SET 
               title = ?, description = ?, start_datetime = ?, end_datetime = ?,
               category_id = ?, subcategory_id = ?
               WHERE id = ?""",
            (
                appointment.title,
                appointment.description,
                appointment.start_datetime.isoformat(),
                appointment.end_datetime.isoformat(),
                appointment.category_id,
                appointment.subcategory_id,
                appointment.id
            )
        )
        
        self.connection.commit()
        return cursor.rowcount > 0
    
    def deleteAppointment(self, appointment_id: int) -> bool:
        """Supprime un rendez-vous"""
        cursor = self.connection.cursor()
        
        cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        
        self.connection.commit()
        return cursor.rowcount > 0
    
    def close(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()