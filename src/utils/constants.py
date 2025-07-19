"""Constants globales pour l'application"""

DATABASE_PATH = "calendar_data.db"
APP_NAME = "Gestion Calendrier"
APP_VERSION = "1.0.0"

DEFAULT_CATEGORIES = {
    "Perso": ["Médical", "Loisirs", "Famille", "Sport"],
    "Pro": ["Réunion", "Formation", "Projet", "Administratif"]
}

COLORS = {
    "Perso": "#3B82F6",  # Bleu
    "Pro": "#EF4444",    # Rouge
    "default": "#6B7280" # Gris
}

TIME_SLOTS = [f"{h:02d}:00" for h in range(24)]