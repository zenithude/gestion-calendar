"""Vue calendrier pour afficher les rendez-vous"""

import customtkinter as ctk
import calendar
from datetime import date, datetime, timedelta
from typing import Callable, Optional, List
from src.services.appointment_service import AppointmentService
from src.models.appointment import Appointment


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
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        self.month_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.month_label.pack(pady=10)
        
        # Frame principal du calendrier
        self.calendar_frame = ctk.CTkFrame(self)
        self.calendar_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Configuration de la grille pour 7 colonnes (jours) et 7 lignes (en-tête + 6 semaines max)
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):
            self.calendar_frame.grid_rowconfigure(i, weight=1)
        
        # En-têtes des jours
        self.createDayHeaders()
        
        # Grille des jours
        self.day_buttons = {}
        self.createDayGrid()
    
    def createDayHeaders(self):
        """Crée les en-têtes des jours de la semaine"""
        days = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        
        for i, day in enumerate(days):
            label = ctk.CTkLabel(
                self.calendar_frame,
                text=day,
                font=ctk.CTkFont(weight="bold")
            )
            label.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
    
    def createDayGrid(self):
        """Crée la grille des jours du mois"""
        # Nettoyer les boutons existants
        for btn in self.day_buttons.values():
            btn.destroy()
        self.day_buttons.clear()
        
        # Obtenir le calendrier du mois
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        row = 1
        for week in cal:
            col = 0
            for day in week:
                if day == 0:
                    # Jour vide (du mois précédent/suivant)
                    empty_frame = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
                    empty_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
                else:
                    # Jour du mois courant
                    day_date = date(self.current_date.year, self.current_date.month, day)
                    self.createDayButton(day_date, row, col)
                
                col += 1
            row += 1
    
    def createDayButton(self, day_date: date, row: int, col: int):
        """Crée un bouton pour un jour spécifique"""
        # Frame container pour le jour
        day_frame = ctk.CTkFrame(self.calendar_frame, height=80)
        day_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        day_frame.grid_propagate(False)
        
        # Déterminer la couleur selon l'état du jour
        is_today = day_date == date.today()
        is_selected = day_date == self.selected_date
        
        if is_today:
            bg_color = "#2563EB"  # Bleu pour aujourd'hui
        elif is_selected:
            bg_color = "#1D4ED8"  # Bleu foncé pour sélectionné
        else:
            bg_color = "#F3F4F6"  # Gris clair par défaut
        
        # Bouton du jour
        day_btn = ctk.CTkButton(
            day_frame,
            text=str(day_date.day),
            width=30,
            height=25,
            fg_color=bg_color,
            command=lambda d=day_date: self.selectDate(d)
        )
        day_btn.pack(pady=(5, 2))
        
        # Indicateur de rendez-vous
        appointments = self.appointment_service.getAppointmentsByDate(day_date)
        if appointments:
            indicator = ctk.CTkLabel(
                day_frame,
                text=f"● {len(appointments)}",
                font=ctk.CTkFont(size=10),
                text_color="#EF4444"
            )
            indicator.pack()
        
        self.day_buttons[day_date] = day_frame
    
    def selectDate(self, selected_date: date):
        """Sélectionne une date et affiche ses rendez-vous"""
        self.selected_date = selected_date
        self.on_date_selected(selected_date)
        
        # Actualiser l'affichage pour mettre en évidence la sélection
        self.createDayGrid()
        
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
        """Affiche un mois/année spécifique"""
        self.current_date = target_date
        self.month_label.configure(
            text=target_date.strftime("%B %Y").capitalize()
        )
        self.createDayGrid()
    
    def refreshView(self):
        """Actualise la vue calendrier"""
        self.createDayGrid()