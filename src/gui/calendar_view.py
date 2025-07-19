"""Vue calendrier pour afficher les rendez-vous"""

import customtkinter as ctk
import calendar
from datetime import date, datetime, timedelta
from typing import Callable, Optional, List
from src.services.appointment_service import AppointmentService
from src.models.appointment import Appointment
from src.utils.theme import getButtonStyle, getFrameStyle, getCalendarCellStyle, SIZES, COLORS, FONTS, CORNER_RADIUS


class CalendarView(ctk.CTkFrame):
    """Widget de vue calendrier mensuelle"""
    
    def __init__(self, parent, appointment_service: AppointmentService, 
                 on_date_selected: Callable, on_appointment_selected: Callable):
        super().__init__(parent)
        
        self.appointment_service = appointment_service
        self.on_date_selected = on_date_selected
        self.on_appointment_selected = on_appointment_selected
        
        self.current_date = date.today()
        self.selected_date = date.today()
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.setupUI()
    
    def setupUI(self):
        """Configure l'interface du calendrier"""
        # En-tête avec titre du mois
        header_style = getFrameStyle("card")
        self.header_frame = ctk.CTkFrame(self, **header_style)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=SIZES["spacing_md"], pady=(SIZES["spacing_md"], SIZES["spacing_sm"]))
        
        self.month_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(size=FONTS["size_xl"], weight=FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        self.month_label.pack(pady=SIZES["spacing_md"])
        
        # Frame principal du calendrier avec style amélioré
        calendar_style = getFrameStyle("default")
        self.calendar_frame = ctk.CTkFrame(self, **calendar_style)
        self.calendar_frame.grid(row=1, column=0, sticky="nsew", padx=SIZES["spacing_md"], pady=(0, SIZES["spacing_md"]))
        
        # Configuration de la grille pour 7 colonnes (jours) et 7 lignes (en-tête + 6 semaines max)
        # IMPORTANT: Assurer des proportions PARFAITEMENT uniformes
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(
                i, 
                weight=1, 
                minsize=SIZES["calendar_cell_size"],
                uniform="calendar_cols"  # Force toutes les colonnes à avoir la même taille
            )
        for i in range(7):
            self.calendar_frame.grid_rowconfigure(
                i, 
                weight=1, 
                minsize=SIZES["calendar_cell_size"],
                uniform="calendar_rows"  # Force toutes les lignes à avoir la même taille
            )
        
        # En-têtes des jours
        self.createDayHeaders()
        
        # Grille des jours - Structure fixe de 6 lignes x 7 colonnes
        self.day_buttons = {}
        self.fixed_cells = {}  # Cache des cellules fixes pour éviter les recreations
        self.createFixedGrid()
        self.updateDayGrid()
    
    def createDayHeaders(self):
        """Crée les en-têtes des jours de la semaine"""
        days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        
        for i, day in enumerate(days):
            # Frame pour chaque en-tête de jour avec style uniforme
            header_frame = ctk.CTkFrame(
                self.calendar_frame, 
                fg_color=COLORS["background_dark"],
                corner_radius=CORNER_RADIUS["calendar_cell"],
                height=SIZES["calendar_cell_size"] // 2
            )
            header_frame.grid(row=0, column=i, padx=SIZES["spacing_xs"], pady=SIZES["spacing_xs"], sticky="nsew")
            header_frame.grid_propagate(False)
            
            label = ctk.CTkLabel(
                header_frame,
                text=day,
                font=ctk.CTkFont(weight=FONTS["weight_bold"], size=FONTS["size_sm"]),
                text_color=COLORS["text_secondary"]
            )
            label.pack(expand=True)
    
    def createFixedGrid(self):
        """Crée une grille fixe de 6x7 cellules qui ne seront jamais détruites"""
        # Créer 6 lignes x 7 colonnes de cellules vides réutilisables
        for row in range(1, 7):  # Lignes 1 à 6 (ligne 0 = en-têtes)
            for col in range(7):  # Colonnes 0 à 6
                cell_key = f"{row}_{col}"
                
                # Créer une cellule fixe vide
                cell_frame = ctk.CTkFrame(
                    self.calendar_frame,
                    width=SIZES["calendar_cell_size"],
                    height=SIZES["calendar_cell_size"],
                    fg_color=COLORS["surface"],
                    corner_radius=CORNER_RADIUS["calendar_cell"]
                )
                cell_frame.grid(
                    row=row, 
                    column=col, 
                    padx=SIZES["spacing_xs"], 
                    pady=SIZES["spacing_xs"], 
                    sticky="nsew",
                    ipadx=2,
                    ipady=2
                )
                cell_frame.grid_propagate(False)
                cell_frame.grid_columnconfigure(0, weight=1)
                cell_frame.grid_rowconfigure(0, weight=1)
                cell_frame.grid_rowconfigure(1, weight=0)
                
                # Créer un bouton réutilisable à l'intérieur
                cell_btn = ctk.CTkButton(
                    cell_frame,
                    text="",
                    font=ctk.CTkFont(size=FONTS["size_md"], weight=FONTS["weight_bold"]),
                    fg_color="transparent",
                    text_color=COLORS["text_primary"],
                    hover_color=COLORS["surface_hover"],
                    corner_radius=0,
                    command=lambda r=row, c=col: self.onCellClick(r, c)
                )
                cell_btn.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
                
                # Créer un label d'indicateur réutilisable
                indicator_frame = ctk.CTkFrame(
                    cell_frame,
                    fg_color="transparent",
                    height=16
                )
                indicator_frame.grid(row=1, column=0, sticky="ew", padx=2, pady=(0, 2))
                indicator_frame.grid_propagate(False)
                
                indicator_label = ctk.CTkLabel(
                    indicator_frame,
                    text="",
                    font=ctk.CTkFont(size=FONTS["size_xs"]),
                    text_color=COLORS["appointment_indicator"]
                )
                indicator_label.pack(expand=True)
                
                # Stocker les références dans le cache
                self.fixed_cells[cell_key] = {
                    'frame': cell_frame,
                    'button': cell_btn,
                    'indicator_frame': indicator_frame,
                    'indicator_label': indicator_label,
                    'date': None,  # Date associée (None = cellule vide)
                    'row': row,
                    'col': col
                }
    
    def updateDayGrid(self):
        """Met à jour le contenu des cellules existantes SANS les recréer"""
        # Vider le mapping jour -> cellule
        self.day_buttons.clear()
        
        # Obtenir le calendrier du mois
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Remplir d'abord toutes les cellules comme vides
        for cell_key, cell_data in self.fixed_cells.items():
            self.updateCellAsEmpty(cell_data)
        
        # Maintenant remplir les cellules avec les jours du mois
        for week_idx, week in enumerate(cal):
            row = week_idx + 1  # +1 car ligne 0 = en-têtes
            for col, day in enumerate(week):
                if day != 0:  # Jour valide du mois
                    cell_key = f"{row}_{col}"
                    if cell_key in self.fixed_cells:
                        day_date = date(self.current_date.year, self.current_date.month, day)
                        self.updateCellWithDay(self.fixed_cells[cell_key], day_date)
                        self.day_buttons[day_date] = self.fixed_cells[cell_key]['frame']
    
    def updateCellAsEmpty(self, cell_data):
        """Met à jour une cellule pour qu'elle soit vide"""
        cell_data['date'] = None
        cell_data['button'].configure(text="", state="disabled")
        cell_data['frame'].configure(fg_color="transparent")
        cell_data['indicator_label'].configure(text="")
    
    def updateCellWithDay(self, cell_data, day_date):
        """Met à jour une cellule avec un jour spécifique"""
        # Déterminer l'état
        is_today = day_date == date.today()
        is_selected = day_date == self.selected_date
        appointments = self.appointment_service.getAppointmentsByDate(day_date)
        has_appointments = len(appointments) > 0
        
        # Obtenir le style
        cell_style = getCalendarCellStyle(is_today, is_selected, has_appointments)
        text_color = cell_style.get("text_color", COLORS["text_primary"])
        fg_color = cell_style.get("fg_color", COLORS["surface"])
        
        # Mettre à jour la cellule
        cell_data['date'] = day_date
        cell_data['frame'].configure(fg_color=fg_color)
        cell_data['button'].configure(
            text=str(day_date.day),
            text_color=text_color,
            state="normal",
            hover_color=COLORS["surface_hover"] if not (is_today or is_selected) else fg_color
        )
        
        # Mettre à jour l'indicateur
        if has_appointments:
            indicator_color = COLORS["appointment_indicator"] if not (is_today or is_selected) else text_color
            cell_data['indicator_label'].configure(
                text=f"● {len(appointments)}",
                text_color=indicator_color
            )
        else:
            cell_data['indicator_label'].configure(text="")
    
    def onCellClick(self, row, col):
        """Gère le clic sur une cellule"""
        cell_key = f"{row}_{col}"
        if cell_key in self.fixed_cells:
            cell_data = self.fixed_cells[cell_key]
            if cell_data['date']:  # Cellule avec un jour valide
                self.selectDate(cell_data['date'])

    def createDayGrid(self):
        """Crée la grille des jours du mois sans flash visible"""
        # TECHNIQUE ANTI-FLASH: Suspendre les mises à jour visuelles
        self.calendar_frame.update_idletasks()
        
        # Nettoyer les boutons existants
        for btn in self.day_buttons.values():
            btn.destroy()
        self.day_buttons.clear()
        
        # Forcer la mise à jour pour éviter l'accumulation
        self.calendar_frame.update_idletasks()
        
        # Obtenir le calendrier du mois
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Créer toutes les cellules en une seule fois pour minimiser les redraws
        widgets_to_create = []
        row = 1
        for week in cal:
            col = 0
            for day in week:
                if day == 0:
                    # Jour vide (du mois précédent/suivant)
                    widgets_to_create.append(('empty', row, col))
                else:
                    # Jour du mois courant
                    day_date = date(self.current_date.year, self.current_date.month, day)
                    widgets_to_create.append(('day', row, col, day_date))
                col += 1
            row += 1
        
        # Créer tous les widgets d'un coup
        for widget_info in widgets_to_create:
            if widget_info[0] == 'empty':
                _, row, col = widget_info
                empty_frame = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
                empty_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            else:
                _, row, col, day_date = widget_info
                self.createDayButton(day_date, row, col)
        
        # Forcer l'affichage final
        self.calendar_frame.update_idletasks()
    
    def createDayButton(self, day_date: date, row: int, col: int):
        """Crée un bouton pour un jour spécifique avec proportions parfaites"""
        # Déterminer l'état du jour
        is_today = day_date == date.today()
        is_selected = day_date == self.selected_date
        appointments = self.appointment_service.getAppointmentsByDate(day_date)
        has_appointments = len(appointments) > 0
        
        # Obtenir le style approprié selon l'état
        cell_style = getCalendarCellStyle(is_today, is_selected, has_appointments)
        
        # Extraire les propriétés spécifiques
        frame_width = cell_style.pop("width", SIZES["calendar_cell_size"])
        frame_height = cell_style.pop("height", SIZES["calendar_cell_size"])
        text_color = cell_style.pop("text_color", COLORS["text_primary"])
        
        # Frame container avec taille fixe pour uniformité PARFAITE
        day_frame = ctk.CTkFrame(
            self.calendar_frame,
            width=frame_width,
            height=frame_height,
            **cell_style  # Maintenant ne contient que fg_color et corner_radius
        )
        day_frame.grid(
            row=row, 
            column=col, 
            padx=SIZES["spacing_xs"], 
            pady=SIZES["spacing_xs"], 
            sticky="nsew",
            ipadx=2,  # Padding interne horizontal pour centrage parfait
            ipady=2   # Padding interne vertical pour centrage parfait
        )
        day_frame.grid_propagate(False)  # Crucial pour maintenir la taille fixe
        
        # Configuration interne du frame
        day_frame.grid_columnconfigure(0, weight=1)
        day_frame.grid_rowconfigure(0, weight=1)
        day_frame.grid_rowconfigure(1, weight=0)  # Pour l'indicateur
        
        # Bouton du jour qui prend toute la place disponible
        day_btn = ctk.CTkButton(
            day_frame,
            text=str(day_date.day),
            font=ctk.CTkFont(size=FONTS["size_md"], weight=FONTS["weight_bold"]),
            fg_color="transparent",  # Transparent pour hériter du frame
            text_color=text_color,
            hover_color=COLORS["surface_hover"] if not (is_today or is_selected) else cell_style.get("fg_color", COLORS["surface"]),
            corner_radius=0,  # Pas de coin pour le bouton interne
            command=lambda d=day_date: self.selectDate(d)
        )
        day_btn.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        # Indicateur de rendez-vous (petit, discret, en bas)
        if has_appointments:
            indicator_frame = ctk.CTkFrame(
                day_frame,
                fg_color="transparent",
                height=16
            )
            indicator_frame.grid(row=1, column=0, sticky="ew", padx=2, pady=(0, 2))
            indicator_frame.grid_propagate(False)
            
            indicator = ctk.CTkLabel(
                indicator_frame,
                text=f"● {len(appointments)}",
                font=ctk.CTkFont(size=FONTS["size_xs"]),
                text_color=COLORS["appointment_indicator"] if not (is_today or is_selected) else text_color
            )
            indicator.pack(expand=True)
        
        self.day_buttons[day_date] = day_frame
    
    def updateCellStates(self, old_selected=None):
        """Met à jour sélectivement les styles des cellules avec le nouveau système"""
        # Avec le nouveau système, on peut juste mettre à jour les cellules concernées
        dates_to_update = []
        
        # Ajouter l'ancienne date sélectionnée si elle existe
        if old_selected:
            dates_to_update.append(old_selected)
        
        # Ajouter la nouvelle date sélectionnée
        if self.selected_date:
            dates_to_update.append(self.selected_date)
        
        # Ajouter aujourd'hui si ce n'est pas déjà dans la liste
        today = date.today()
        if today not in dates_to_update:
            dates_to_update.append(today)
        
        # Mettre à jour seulement les cellules concernées
        for day_date in dates_to_update:
            self.updateSingleCellInFixedGrid(day_date)
    
    def updateSingleCellInFixedGrid(self, day_date: date):
        """Met à jour une seule cellule dans la grille fixe"""
        # Trouver la cellule qui contient cette date
        for cell_data in self.fixed_cells.values():
            if cell_data['date'] == day_date:
                self.updateCellWithDay(cell_data, day_date)
                break
    
    def selectDate(self, selected_date: date):
        """Sélectionne une date et affiche ses rendez-vous"""
        old_selected = self.selected_date
        self.selected_date = selected_date
        self.on_date_selected(selected_date)
        
        # Mise à jour sélective SANS redessiner tout le calendrier
        self.updateCellStates(old_selected)
        
        # Afficher les rendez-vous du jour dans une vue timeline
        self.showDayTimeline(selected_date)
    
    def showDayTimeline(self, target_date: date):
        """Affiche la timeline du jour sélectionné"""
        # Cette méthode peut ouvrir une nouvelle fenêtre ou mise à jour une zone dédiée
        appointments = self.appointment_service.getAppointmentsByDate(target_date)
        
        if appointments:
            # Pour l'instant, on utilise une fenêtre popup simple
            timeline_window = ctk.CTkToplevel(self)
            timeline_window.title(f"Rendez-vous du {target_date.strftime('%d/%m/%Y')}")
            timeline_window.geometry("600x400")
            
            # Liste des rendez-vous
            appointments_frame = ctk.CTkScrollableFrame(timeline_window)
            appointments_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            for appointment in appointments:
                self.createAppointmentCard(appointments_frame, appointment)
    
    def createAppointmentCard(self, parent, appointment: Appointment):
        """Crée une carte pour un rendez-vous"""
        card_frame = ctk.CTkFrame(parent)
        card_frame.pack(fill="x", pady=5)
        
        # En-tête avec heure et titre
        header_frame = ctk.CTkFrame(card_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        time_label = ctk.CTkLabel(
            header_frame,
            text=appointment.start_datetime.strftime("%H:%M"),
            font=ctk.CTkFont(weight="bold")
        )
        time_label.pack(side="left")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=appointment.title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(side="left", padx=(10, 0))
        
        # Description si disponible
        if appointment.description:
            desc_label = ctk.CTkLabel(
                card_frame,
                text=appointment.description,
                wraplength=400
            )
            desc_label.pack(padx=10, pady=(0, 5), anchor="w")
        
        # Bouton d'édition
        edit_btn = ctk.CTkButton(
            card_frame,
            text="Modifier",
            width=80,
            height=25,
            command=lambda: self.on_appointment_selected(appointment)
        )
        edit_btn.pack(side="right", padx=10, pady=(0, 10))
    
    def showDate(self, target_date: date):
        """Affiche un mois/année spécifique SANS AUCUN FLASH"""
        old_selected = self.selected_date
        self.current_date = target_date
        self.selected_date = target_date  # Sélectionner la nouvelle date
        
        self.month_label.configure(
            text=target_date.strftime("%B %Y").capitalize()
        )
        
        # NOUVELLE APPROCHE: Toujours utiliser updateDayGrid (pas de flash)
        # Que ce soit un changement de mois ou pas, cette méthode ne recrée rien
        self.updateDayGrid()
    
    def refreshView(self):
        """Actualise la vue calendrier"""
        self.updateDayGrid()