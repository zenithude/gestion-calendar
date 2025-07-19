"""Vue timeline pour afficher les rendez-vous par heure"""

import customtkinter as ctk
from datetime import date, datetime, time
from typing import List, Callable
from src.services.appointment_service import AppointmentService
from src.models.appointment import Appointment


class TimelineView(ctk.CTkFrame):
    """Widget de vue timeline pour afficher les rendez-vous d'une journée"""
    
    def __init__(self, parent, appointment_service: AppointmentService, 
                 on_appointment_selected: Callable):
        super().__init__(parent)
        
        self.appointment_service = appointment_service
        self.on_appointment_selected = on_appointment_selected
        
        self.current_date = date.today()
        self.time_slots = []
        
        self.setupUI()
    
    def setupUI(self):
        """Configure l'interface de la timeline"""
        # En-tête avec date
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        self.date_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.date_label.pack(pady=10)
        
        # Frame scrollable pour la timeline
        self.timeline_frame = ctk.CTkScrollableFrame(self)
        self.timeline_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.createTimeline()
    
    def createTimeline(self):
        """Crée la grille horaire de la journée"""
        # Nettoyer la timeline existante
        for widget in self.timeline_frame.winfo_children():
            widget.destroy()
        
        self.time_slots.clear()
        
        # Créer les créneaux horaires (de 6h à 23h)
        for hour in range(6, 24):
            self.createTimeSlot(hour)
    
    def createTimeSlot(self, hour: int):
        """Crée un créneau horaire"""
        slot_frame = ctk.CTkFrame(self.timeline_frame, height=60)
        slot_frame.pack(fill="x", pady=2)
        slot_frame.pack_propagate(False)
        
        # Configuration de la grille
        slot_frame.grid_columnconfigure(1, weight=1)
        
        # Étiquette de l'heure
        time_label = ctk.CTkLabel(
            slot_frame,
            text=f"{hour:02d}:00",
            font=ctk.CTkFont(weight="bold"),
            width=60
        )
        time_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nw")
        
        # Zone pour les rendez-vous de cette heure
        appointments_frame = ctk.CTkFrame(slot_frame, fg_color="transparent")
        appointments_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=5)
        
        # Ligne de séparation
        separator = ctk.CTkFrame(slot_frame, height=1, fg_color="#E5E7EB")
        separator.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.time_slots.append({
            'hour': hour,
            'frame': slot_frame,
            'appointments_frame': appointments_frame
        })
    
    def showDate(self, target_date: date):
        """Affiche les rendez-vous d'une date spécifique"""
        self.current_date = target_date
        self.date_label.configure(
            text=target_date.strftime("%A %d %B %Y").capitalize()
        )
        
        # Récupérer les rendez-vous du jour
        appointments = self.appointment_service.getAppointmentsByDate(target_date)
        
        # Placer les rendez-vous dans les créneaux appropriés
        self.placeAppointments(appointments)
    
    def placeAppointments(self, appointments: List[Appointment]):
        """Place les rendez-vous dans les créneaux horaires appropriés"""
        # Nettoyer les rendez-vous existants
        for slot in self.time_slots:
            for widget in slot['appointments_frame'].winfo_children():
                widget.destroy()
        
        # Placer chaque rendez-vous
        for appointment in appointments:
            hour = appointment.start_datetime.hour
            
            # Trouver le créneau correspondant
            slot = next((s for s in self.time_slots if s['hour'] == hour), None)
            
            if slot:
                self.createAppointmentWidget(slot['appointments_frame'], appointment)
    
    def createAppointmentWidget(self, parent, appointment: Appointment):
        """Crée un widget pour afficher un rendez-vous"""
        # Frame principal du rendez-vous
        apt_frame = ctk.CTkFrame(parent)
        apt_frame.pack(fill="x", pady=2)
        
        # Configuration de la grille
        apt_frame.grid_columnconfigure(1, weight=1)
        
        # Indicateur coloré (selon la catégorie)
        color_indicator = ctk.CTkFrame(apt_frame, width=4, fg_color="#3B82F6")
        color_indicator.grid(row=0, column=0, sticky="ns", padx=(5, 0))
        
        # Contenu du rendez-vous
        content_frame = ctk.CTkFrame(apt_frame, fg_color="transparent")
        content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        
        # En-tête avec heure et titre
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x")
        
        time_text = f"{appointment.start_datetime.strftime('%H:%M')}"
        if appointment.end_datetime:
            time_text += f" - {appointment.end_datetime.strftime('%H:%M')}"
        
        time_label = ctk.CTkLabel(
            header_frame,
            text=time_text,
            font=ctk.CTkFont(size=10),
            text_color="#6B7280"
        )
        time_label.pack(side="left")
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=appointment.title,
            font=ctk.CTkFont(weight="bold")
        )
        title_label.pack(side="left", padx=(10, 0))
        
        # Description (si disponible et courte)
        if appointment.description and len(appointment.description) < 100:
            desc_label = ctk.CTkLabel(
                content_frame,
                text=appointment.description,
                font=ctk.CTkFont(size=10),
                text_color="#6B7280",
                wraplength=300
            )
            desc_label.pack(anchor="w", pady=(2, 0))
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(5, 0))
        
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Modifier",
            width=60,
            height=20,
            font=ctk.CTkFont(size=10),
            command=lambda: self.on_appointment_selected(appointment)
        )
        edit_btn.pack(side="right")
        
        # Interaction: clic pour sélectionner
        def selectAppointment(event=None):
            self.on_appointment_selected(appointment)
        
        apt_frame.bind("<Button-1>", selectAppointment)
        content_frame.bind("<Button-1>", selectAppointment)
    
    def addNewAppointmentSlot(self, hour: int):
        """Ajoute un slot pour créer un nouveau rendez-vous à une heure donnée"""
        slot = next((s for s in self.time_slots if s['hour'] == hour), None)
        
        if slot:
            add_frame = ctk.CTkFrame(slot['appointments_frame'], fg_color="#F9FAFB")
            add_frame.pack(fill="x", pady=2)
            
            add_btn = ctk.CTkButton(
                add_frame,
                text=f"+ Nouveau RDV à {hour:02d}:00",
                height=25,
                fg_color="#10B981",
                command=lambda: self.createAppointmentAt(hour)
            )
            add_btn.pack(padx=10, pady=5)
    
    def createAppointmentAt(self, hour: int):
        """Déclenche la création d'un nouveau rendez-vous à une heure donnée"""
        # Cette méthode devrait déclencher l'ouverture du dialogue de création
        # avec l'heure pré-remplie
        suggested_datetime = datetime.combine(
            self.current_date, 
            time(hour, 0)
        )
        
        # Appeler le callback parent avec la suggestion d'heure
        if hasattr(self, 'on_new_appointment'):
            self.on_new_appointment(suggested_datetime)
    
    def refreshView(self):
        """Actualise la vue timeline"""
        self.showDate(self.current_date)