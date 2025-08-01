"""Fenêtre principale de l'application"""

import customtkinter as ctk
from datetime import datetime, date
from typing import Optional
from src.services.category_service import CategoryService
from src.services.appointment_service import AppointmentService
from src.gui.calendar_view import CalendarView
from src.gui.timeline_view import TimelineView
from src.gui.appointment_dialog import AppointmentDialog
from src.utils.constants import APP_NAME, APP_VERSION
from src.utils.theme import getButtonStyle, getFrameStyle, SIZES, COLORS, FONTS, CORNER_RADIUS


class MainWindow:
    """Fenêtre principale de l'application de gestion de calendrier"""
    
    def __init__(self, category_service: CategoryService, appointment_service: AppointmentService):
        self.category_service = category_service
        self.appointment_service = appointment_service
        
        # Configuration du thème
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Variables d'état
        self.current_date = date.today()
        self.selected_appointment = None
        
        # Initialiser l'interface
        self.setupUI()
        self.setupBindings()
    
    def setupUI(self):
        """Configure l'interface utilisateur"""
        # Frame principal avec sidebar et content
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configuration de la grille
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Sidebar gauche
        self.createSidebar()
        
        # Zone de contenu principale
        self.createContentArea()
        
        # Barre de statut
        self.createStatusBar()
    
    def createSidebar(self):
        """Crée la barre latérale avec les contrôles"""
        sidebar_style = getFrameStyle("sidebar")
        self.sidebar = ctk.CTkFrame(
            self.main_frame, 
            width=SIZES["sidebar_width"],
            **sidebar_style
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, SIZES["spacing_md"]))
        self.sidebar.grid_propagate(False)
        
        # Titre de l'application
        title_label = ctk.CTkLabel(
            self.sidebar, 
            text=APP_NAME,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        title_label.pack(pady=(SIZES["spacing_xl"], SIZES["spacing_xxl"]))
        
        # Navigation temporelle
        nav_frame_style = getFrameStyle("card")
        nav_frame = ctk.CTkFrame(self.sidebar, **nav_frame_style)
        nav_frame.pack(fill="x", padx=SIZES["spacing_xl"], pady=(0, SIZES["spacing_xl"]))
        
        nav_label = ctk.CTkLabel(
            nav_frame, 
            text="Navigation", 
            font=ctk.CTkFont(weight="bold"),
            text_color=COLORS["text_primary"]
        )
        nav_label.pack(pady=(SIZES["spacing_md"], SIZES["spacing_sm"]))
        
        # Boutons de navigation
        nav_buttons_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        nav_buttons_frame.pack(fill="x", padx=SIZES["spacing_md"], pady=(0, SIZES["spacing_md"]))
        
        # Boutons précédent et suivant parfaitement carrés (angles ratés résolus)
        nav_btn_style = getButtonStyle("primary", "small")
        nav_btn_style["corner_radius"] = 0  # CARRÉ pour éviter les angles ratés
        
        prev_btn = ctk.CTkButton(
            nav_buttons_frame, 
            text="◀", 
            width=SIZES["button_height"],
            command=self.previousPeriod,
            **nav_btn_style
        )
        prev_btn.pack(side="left", padx=(0, SIZES["spacing_sm"]))
        
        self.date_label = ctk.CTkLabel(
            nav_buttons_frame, 
            text=self.current_date.strftime("%B %Y"),
            font=ctk.CTkFont(weight="bold"),
            text_color=COLORS["text_primary"]
        )
        self.date_label.pack(side="left", expand=True)
        
        next_btn = ctk.CTkButton(
            nav_buttons_frame, 
            text="▶", 
            width=SIZES["button_height"],
            command=self.nextPeriod,
            **nav_btn_style
        )
        next_btn.pack(side="right", padx=(SIZES["spacing_sm"], 0))
        
        # Bouton aujourd'hui parfaitement carré (angles ratés résolus)
        today_btn_style = getButtonStyle("secondary")
        today_btn_style["corner_radius"] = 0  # CARRÉ pour éviter les angles ratés
        today_btn = ctk.CTkButton(
            nav_frame,
            text="Aujourd'hui",
            command=self.goToToday,
            **today_btn_style
        )
        today_btn.pack(pady=(0, SIZES["spacing_md"]))
        
        # Actions
        actions_frame_style = getFrameStyle("card")
        actions_frame = ctk.CTkFrame(self.sidebar, **actions_frame_style)
        actions_frame.pack(fill="x", padx=SIZES["spacing_xl"], pady=(0, SIZES["spacing_xl"]))
        
        actions_label = ctk.CTkLabel(
            actions_frame, 
            text="Actions", 
            font=ctk.CTkFont(weight="bold"),
            text_color=COLORS["text_primary"]
        )
        actions_label.pack(pady=(SIZES["spacing_md"], SIZES["spacing_sm"]))
        
        # Bouton nouveau rendez-vous parfaitement carré (angles ratés résolus)
        new_appointment_btn_style = getButtonStyle("success")
        new_appointment_btn_style["corner_radius"] = 0  # CARRÉ pour éviter les angles ratés
        new_appointment_btn = ctk.CTkButton(
            actions_frame,
            text="+ Nouveau RDV",
            command=self.createNewAppointment,
            **new_appointment_btn_style
        )
        new_appointment_btn.pack(fill="x", padx=SIZES["spacing_md"], pady=(0, SIZES["spacing_md"]))
        
        # Filtres par catégorie
        filters_frame_style = getFrameStyle("card")
        filters_frame = ctk.CTkFrame(self.sidebar, **filters_frame_style)
        filters_frame.pack(fill="x", padx=SIZES["spacing_xl"], pady=(0, SIZES["spacing_xl"]))
        
        filters_label = ctk.CTkLabel(
            filters_frame, 
            text="Filtres", 
            font=ctk.CTkFont(weight="bold"),
            text_color=COLORS["text_primary"]
        )
        filters_label.pack(pady=(SIZES["spacing_md"], SIZES["spacing_sm"]))
        
        # Checkboxes pour les catégories avec style amélioré et bordure visible
        categories = self.category_service.getAllCategories()
        for category in categories:
            checkbox = ctk.CTkCheckBox(
                filters_frame, 
                text=category.name,
                command=lambda: self.updateCalendarView(),
                text_color=COLORS["text_primary"],
                # SOLUTION: Bordure toujours visible + remplissage qui change
                fg_color=COLORS["primary"],              # Couleur quand coché (bleu)
                hover_color=COLORS["primary_hover"],     # Couleur au survol
                checkmark_color=COLORS["text_inverse"],  # Couleur de la coche (blanc)
                border_color=COLORS["primary"],          # Bordure toujours bleue
                border_width=2,                          # Bordure épaisse et visible
                corner_radius=0,  # CARRÉ pour cohérence avec tous les boutons sidebar
                font=ctk.CTkFont(size=FONTS["size_md"], weight=FONTS["weight_normal"])
            )
            checkbox.pack(anchor="w", padx=SIZES["spacing_md"], pady=SIZES["spacing_xs"])
            checkbox.select()  # Sélectionné par défaut
    
    def createContentArea(self):
        """Crée la zone de contenu principal"""
        content_style = getFrameStyle("default")
        self.content_frame = ctk.CTkFrame(self.main_frame, **content_style)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Vue calendrier
        self.calendar_view = CalendarView(
            self.content_frame, 
            self.appointment_service,
            self.onDateSelected,
            self.onAppointmentSelected
        )
        self.calendar_view.pack(fill="both", expand=True, padx=SIZES["spacing_md"], pady=SIZES["spacing_md"])
        
        # Initialiser avec la date courante
        self.calendar_view.showDate(self.current_date)
    
    def createStatusBar(self):
        """Crée la barre de statut"""
        status_style = getFrameStyle("card")
        self.status_frame = ctk.CTkFrame(self.main_frame, height=30, **status_style)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(SIZES["spacing_md"], 0))
        self.status_frame.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text=f"Prêt - {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            text_color=COLORS["text_secondary"],
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=SIZES["spacing_md"], pady=SIZES["spacing_sm"])
    
    def setupBindings(self):
        """Configure les raccourcis clavier"""
        self.root.bind("<Control-n>", lambda e: self.createNewAppointment())
        self.root.bind("<F5>", lambda e: self.updateCalendarView())
        self.root.bind("<Escape>", lambda e: self.root.quit())
    
    def onDateSelected(self, selected_date: date):
        """Callback appelé quand une date est sélectionnée"""
        self.current_date = selected_date
        self.date_label.configure(text=selected_date.strftime("%B %Y"))
        self.updateStatusBar(f"Date sélectionnée: {selected_date.strftime('%d/%m/%Y')}")
    
    def onAppointmentSelected(self, appointment):
        """Callback appelé quand un rendez-vous est sélectionné"""
        self.selected_appointment = appointment
        if appointment:
            self.updateStatusBar(f"RDV sélectionné: {appointment.title}")
            # Double-clic pour éditer
            self.editAppointment(appointment)
    
    def previousPeriod(self):
        """Navigate vers la période précédente"""
        # Logique de navigation (mois précédent par exemple)
        if self.current_date.month == 1:
            new_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            new_date = self.current_date.replace(month=self.current_date.month - 1)
        
        self.current_date = new_date
        self.calendar_view.showDate(new_date)
        self.date_label.configure(text=new_date.strftime("%B %Y"))
    
    def nextPeriod(self):
        """Navigate vers la période suivante"""
        # Logique de navigation (mois suivant par exemple)
        if self.current_date.month == 12:
            new_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            new_date = self.current_date.replace(month=self.current_date.month + 1)
        
        self.current_date = new_date
        self.calendar_view.showDate(new_date)
        self.date_label.configure(text=new_date.strftime("%B %Y"))
    
    def goToToday(self):
        """Revient à la date d'aujourd'hui"""
        today = date.today()
        self.current_date = today
        self.calendar_view.showDate(today)
        self.date_label.configure(text=today.strftime("%B %Y"))
        self.updateStatusBar("Navigation: Aujourd'hui")
    
    def createNewAppointment(self):
        """Ouvre le dialogue de création d'un nouveau rendez-vous"""
        dialog = AppointmentDialog(
            self.root,
            self.category_service,
            self.appointment_service,
            appointment=None,  # Nouveau rendez-vous
            callback=self.onAppointmentSaved
        )
        dialog.show()
    
    def editAppointment(self, appointment):
        """Ouvre le dialogue d'édition d'un rendez-vous"""
        dialog = AppointmentDialog(
            self.root,
            self.category_service,
            self.appointment_service,
            appointment=appointment,
            callback=self.onAppointmentSaved
        )
        dialog.show()
    
    def onAppointmentSaved(self, appointment_data):
        """Callback appelé quand un rendez-vous est sauvegardé"""
        # Actualiser la vue
        self.updateCalendarView()
        self.updateStatusBar("Rendez-vous sauvegardé")
    
    def updateCalendarView(self):
        """Met à jour la vue calendrier"""
        self.calendar_view.showDate(self.current_date)
    
    def updateStatusBar(self, message: str):
        """Met à jour la barre de statut"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.status_label.configure(text=f"{message} - {timestamp}")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()