"""Système de thème centralisé pour l'application"""

# =============================================================================
# CORNER RADIUS - Standardisation des angles arrondis
# =============================================================================

CORNER_RADIUS = {
    # Boutons standards - Valeurs optimisées pour un rendu net
    "button": 6,           # Réduit de 8 à 6 pour éviter les artefacts
    "button_small": 4,     # Réduit de 6 à 4
    "button_large": 8,     # Réduit de 10 à 8
    
    # Frames et containers
    "frame": 10,           # Réduit de 12 à 10
    "card": 6,             # Réduit de 8 à 6
    "sidebar": 12,         # Réduit de 16 à 12
    
    # Dialogues et fenêtres
    "dialog": 12,          # Réduit de 16 à 12
    "popup": 8,            # Réduit de 12 à 8
    
    # Éléments spéciaux
    "calendar_cell": 4,    # Réduit de 6 à 4
    "timeline_slot": 6,    # Réduit de 8 à 6
    "checkbox": 2          # Réduit de 4 à 2 pour les checkboxes
}

# =============================================================================
# COULEURS - Palette cohérente et moderne
# =============================================================================

COLORS = {
    # Couleurs primaires
    "primary": "#3B82F6",      # Bleu principal
    "primary_hover": "#2563EB", # Bleu au survol
    "primary_dark": "#1D4ED8",  # Bleu foncé
    
    # Couleurs secondaires
    "secondary": "#6B7280",     # Gris neutre
    "secondary_light": "#9CA3AF", # Gris clair
    "secondary_dark": "#374151", # Gris foncé
    
    # Couleurs de statut
    "success": "#10B981",       # Vert succès
    "success_hover": "#059669", # Vert succès hover
    "error": "#EF4444",         # Rouge erreur
    "error_hover": "#DC2626",   # Rouge erreur hover
    "warning": "#F59E0B",       # Orange avertissement
    "info": "#06B6D4",          # Cyan info
    
    # Couleurs de catégories
    "category_perso": "#3B82F6", # Bleu pour personnel
    "category_pro": "#EF4444",   # Rouge pour professionnel
    "category_default": "#6B7280", # Gris par défaut
    
    # Couleurs de fond
    "background": "#F9FAFB",     # Fond principal
    "background_dark": "#F3F4F6", # Fond secondaire
    "surface": "#FFFFFF",        # Surface des cartes
    "surface_hover": "#F8FAFC",  # Surface au survol
    
    # Couleurs de bordure
    "border": "#E5E7EB",         # Bordure standard
    "border_focus": "#3B82F6",   # Bordure au focus
    "border_error": "#EF4444",   # Bordure d'erreur
    
    # Couleurs de texte
    "text_primary": "#111827",   # Texte principal
    "text_secondary": "#6B7280", # Texte secondaire
    "text_muted": "#9CA3AF",     # Texte atténué
    "text_inverse": "#FFFFFF",   # Texte inversé (sur fond sombre)
    
    # Couleurs spéciales calendrier
    "today": "#2563EB",          # Couleur pour aujourd'hui
    "selected": "#1D4ED8",       # Couleur pour sélectionné
    "weekend": "#F3F4F6",        # Couleur pour week-end
    "appointment_indicator": "#EF4444" # Indicateur de rendez-vous
}

# =============================================================================
# DIMENSIONS - Tailles standardisées
# =============================================================================

SIZES = {
    # Boutons
    "button_height": 32,         # Hauteur standard des boutons
    "button_height_small": 24,   # Petits boutons
    "button_height_large": 40,   # Grands boutons
    "button_width_min": 80,      # Largeur minimale
    
    # Espacement
    "spacing_xs": 4,             # Très petit espacement
    "spacing_sm": 8,             # Petit espacement
    "spacing_md": 12,            # Espacement moyen
    "spacing_lg": 16,            # Grand espacement
    "spacing_xl": 20,            # Très grand espacement
    "spacing_xxl": 24,           # Espacement extra large
    
    # Conteneurs
    "sidebar_width": 250,        # Largeur de la sidebar
    "dialog_width": 600,         # Largeur des dialogues
    "dialog_height": 750,        # Hauteur des dialogues
    
    # Calendrier
    "calendar_cell_size": 80,    # Taille des cellules du calendrier
    "calendar_cell_min": 60,     # Taille minimale des cellules
    
    # Timeline
    "timeline_slot_height": 60,  # Hauteur des créneaux timeline
    "timeline_time_width": 60,   # Largeur de l'affichage heure
    
    # Bordures
    "border_width": 1,           # Épaisseur de bordure standard
    "border_width_thick": 2,     # Bordure épaisse
}

# =============================================================================
# POLICES - Typographie cohérente
# =============================================================================

FONTS = {
    # Tailles de police
    "size_xs": 10,               # Très petite
    "size_sm": 12,               # Petite
    "size_md": 14,               # Moyenne (par défaut)
    "size_lg": 16,               # Grande
    "size_xl": 18,               # Très grande
    "size_xxl": 20,              # Extra large
    "size_title": 24,            # Titre principal
    
    # Poids de police
    "weight_normal": "normal",   # Normal
    "weight_bold": "bold",       # Gras
}

# =============================================================================
# ANIMATIONS - Durées d'animation
# =============================================================================

ANIMATIONS = {
    "duration_fast": 150,        # Animation rapide (ms)
    "duration_normal": 250,      # Animation normale (ms)
    "duration_slow": 400,        # Animation lente (ms)
}

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def getButtonStyle(variant="default", size="normal"):
    """Retourne les paramètres de style pour un bouton
    
    Args:
        variant: "default", "primary", "secondary", "success", "error", "warning"
        size: "small", "normal", "large"
    
    Returns:
        dict: Paramètres de style pour CTkButton
    """
    
    # Couleurs selon la variante
    color_map = {
        "default": COLORS["secondary"],
        "primary": COLORS["primary"],
        "secondary": COLORS["secondary"],
        "success": COLORS["success"],
        "error": COLORS["error"],
        "warning": COLORS["warning"]
    }
    
    hover_map = {
        "default": COLORS["secondary_dark"],
        "primary": COLORS["primary_hover"],
        "secondary": COLORS["secondary_dark"],
        "success": COLORS["success_hover"],
        "error": COLORS["error_hover"],
        "warning": COLORS["warning"]
    }
    
    # Tailles selon le type
    height_map = {
        "small": SIZES["button_height_small"],
        "normal": SIZES["button_height"],
        "large": SIZES["button_height_large"]
    }
    
    corner_map = {
        "small": CORNER_RADIUS["button_small"],
        "normal": CORNER_RADIUS["button"],
        "large": CORNER_RADIUS["button_large"]
    }
    
    return {
        "fg_color": color_map.get(variant, COLORS["secondary"]),
        "hover_color": hover_map.get(variant, COLORS["secondary_dark"]),
        "text_color": COLORS["text_inverse"],
        "corner_radius": corner_map.get(size, CORNER_RADIUS["button"]),
        "height": height_map.get(size, SIZES["button_height"]),
        # Paramètres additionnels pour un rendu parfait
        "border_width": 0,        # Éliminer les bordures qui causent des artefacts
        "anchor": "center"        # Centrage parfait du texte
    }

def getFrameStyle(variant="default"):
    """Retourne les paramètres de style pour un frame
    
    Args:
        variant: "default", "card", "sidebar", "dialog"
    
    Returns:
        dict: Paramètres de style pour CTkFrame
    """
    
    corner_map = {
        "default": CORNER_RADIUS["frame"],
        "card": CORNER_RADIUS["card"],
        "sidebar": CORNER_RADIUS["sidebar"],
        "dialog": CORNER_RADIUS["dialog"]
    }
    
    return {
        "fg_color": COLORS["surface"],
        "corner_radius": corner_map.get(variant, CORNER_RADIUS["frame"]),
        "border_width": 0,  # Désactiver les bordures pour un rendu plus net
        "border_color": COLORS["border"]
    }

def getCalendarCellStyle(is_today=False, is_selected=False, has_appointments=False):
    """Retourne les paramètres de style pour une cellule de calendrier
    
    Args:
        is_today: Si c'est aujourd'hui
        is_selected: Si la cellule est sélectionnée
        has_appointments: Si la cellule a des rendez-vous
    
    Returns:
        dict: Paramètres de style pour la cellule
    """
    
    if is_today:
        fg_color = COLORS["today"]
        text_color = COLORS["text_inverse"]
    elif is_selected:
        fg_color = COLORS["selected"]
        text_color = COLORS["text_inverse"]
    else:
        fg_color = COLORS["surface"]
        text_color = COLORS["text_primary"]
    
    return {
        "fg_color": fg_color,
        "text_color": text_color,
        "corner_radius": CORNER_RADIUS["calendar_cell"],
        "height": SIZES["calendar_cell_size"],
        "width": SIZES["calendar_cell_size"]
    }

# =============================================================================
# CONSTANTES DE MIGRATION
# =============================================================================

# Pour faciliter la migration, on exporte aussi les anciennes constantes
DEFAULT_CATEGORIES = {
    "Perso": ["Médical", "Loisirs", "Famille", "Sport"],
    "Pro": ["Réunion", "Formation", "Projet", "Administratif"]
}

# Mapping des anciennes couleurs vers les nouvelles
LEGACY_COLORS = {
    "Perso": COLORS["category_perso"],
    "Pro": COLORS["category_pro"],
    "default": COLORS["category_default"]
}