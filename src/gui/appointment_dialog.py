"""Dialogue pour créer/éditer des rendez-vous"""

import customtkinter as ctk
from datetime import datetime, date, time
from typing import Optional, Callable, List
from src.services.category_service import CategoryService
from src.models.appointment import Appointment
from src.models.category import Category
from src.models.subcategory import Subcategory


class AppointmentDialog:
    """Dialogue pour la création et modification de rendez-vous"""
    
    def __init__(self, parent, category_service: CategoryService, 
                 appointment: Optional[Appointment] = None, 
                 callback: Optional[Callable] = None):
        self.parent = parent
        self.category_service = category_service
        self.appointment = appointment  # None pour création, objet pour édition
        self.callback = callback
        
        self.window = None
        self.is_editing = appointment is not None
        
        # Variables pour les champs
        self.title_var = ctk.StringVar()
        self.description_var = ctk.StringVar()
        self.date_var = ctk.StringVar()
        self.start_time_var = ctk.StringVar()
        self.end_time_var = ctk.StringVar()
        self.category_var = ctk.StringVar()
        self.subcategory_var = ctk.StringVar()
        
        # Widgets
        self.category_combo = None
        self.subcategory_combo = None
        
        self.categories = []
        self.current_subcategories = []
    
    def show(self):
        """Affiche le dialogue"""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Modifier le rendez-vous" if self.is_editing else "Nouveau rendez-vous")
        self.window.geometry("500x600")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Centrer la fenêtre
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"500x600+{x}+{y}")
        
        self.setupUI()
        self.loadData()
    
    def setupUI(self):
        """Configure l'interface du dialogue"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ctk.CTkLabel(
            main_frame,
            text="Modifier le rendez-vous" if self.is_editing else "Créer un nouveau rendez-vous",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Formulaire
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Titre du rendez-vous
        ctk.CTkLabel(form_frame, text="Titre *", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        title_entry = ctk.CTkEntry(form_frame, textvariable=self.title_var, placeholder_text="Ex: Rendez-vous médecin")
        title_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Description
        ctk.CTkLabel(form_frame, text="Description", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        description_entry = ctk.CTkTextbox(form_frame, height=80)
        description_entry.pack(fill="x", padx=20, pady=(0, 10))
        self.description_textbox = description_entry
        
        # Date
        ctk.CTkLabel(form_frame, text="Date *", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        date_entry = ctk.CTkEntry(form_frame, textvariable=self.date_var, placeholder_text="JJ/MM/AAAA")
        date_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Heures (frame horizontal)
        time_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        time_frame.pack(fill="x", padx=20, pady=(10, 10))
        time_frame.grid_columnconfigure(0, weight=1)
        time_frame.grid_columnconfigure(1, weight=1)
        
        # Heure de début
        start_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        start_frame.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkLabel(start_frame, text="Heure début *", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        start_time_entry = ctk.CTkEntry(start_frame, textvariable=self.start_time_var, placeholder_text="HH:MM")
        start_time_entry.pack(fill="x", pady=(5, 0))
        
        # Heure de fin
        end_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        end_frame.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        ctk.CTkLabel(end_frame, text="Heure fin *", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        end_time_entry = ctk.CTkEntry(end_frame, textvariable=self.end_time_var, placeholder_text="HH:MM")
        end_time_entry.pack(fill="x", pady=(5, 0))
        
        # Catégorie
        ctk.CTkLabel(form_frame, text="Catégorie *", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.category_combo = ctk.CTkComboBox(
            form_frame, 
            values=[],
            command=self.onCategoryChanged
        )
        self.category_combo.pack(fill="x", padx=20, pady=(0, 10))
        
        # Sous-catégorie
        ctk.CTkLabel(form_frame, text="Sous-catégorie", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=(10, 5))
        self.subcategory_combo = ctk.CTkComboBox(form_frame, values=[])
        self.subcategory_combo.pack(fill="x", padx=20, pady=(0, 20))
        
        # Boutons d'action
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Annuler",
            fg_color="#6B7280",
            command=self.cancel
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Modifier" if self.is_editing else "Créer",
            command=self.save
        )
        save_btn.pack(side="right")
        
        # Bouton supprimer (seulement en mode édition)
        if self.is_editing:
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="Supprimer",
                fg_color="#EF4444",
                command=self.delete
            )
            delete_btn.pack(side="left")
    
    def loadData(self):
        """Charge les données dans le formulaire"""
        # Charger les catégories
        self.categories = self.category_service.getAllCategories()
        category_names = [cat.name for cat in self.categories]
        self.category_combo.configure(values=category_names)
        
        if self.is_editing and self.appointment:
            # Mode édition: remplir avec les données existantes
            self.title_var.set(self.appointment.title)
            self.description_textbox.insert("1.0", self.appointment.description or "")
            self.date_var.set(self.appointment.start_datetime.strftime("%d/%m/%Y"))
            self.start_time_var.set(self.appointment.start_datetime.strftime("%H:%M"))
            if self.appointment.end_datetime:
                self.end_time_var.set(self.appointment.end_datetime.strftime("%H:%M"))
            
            # Sélectionner la catégorie
            category = self.category_service.getCategoryById(self.appointment.category_id)
            if category:
                self.category_combo.set(category.name)
                self.onCategoryChanged(category.name)
                
                # Sélectionner la sous-catégorie si disponible
                if self.appointment.subcategory_id:
                    subcategories = self.category_service.getSubcategoriesByCategory(category.id)
                    subcategory = next((sub for sub in subcategories if sub.id == self.appointment.subcategory_id), None)
                    if subcategory:
                        self.subcategory_combo.set(subcategory.name)
        else:
            # Mode création: valeurs par défaut
            today = date.today()
            self.date_var.set(today.strftime("%d/%m/%Y"))
            current_hour = datetime.now().hour
            self.start_time_var.set(f"{current_hour:02d}:00")
            self.end_time_var.set(f"{current_hour + 1:02d}:00")
            
            # Sélectionner la première catégorie par défaut
            if category_names:
                self.category_combo.set(category_names[0])
                self.onCategoryChanged(category_names[0])
    
    def onCategoryChanged(self, category_name: str):
        """Callback appelé quand la catégorie change"""
        # Trouver la catégorie sélectionnée
        category = next((cat for cat in self.categories if cat.name == category_name), None)
        
        if category:
            # Charger les sous-catégories
            subcategories = self.category_service.getSubcategoriesByCategory(category.id)
            subcategory_names = [sub.name for sub in subcategories]
            
            self.current_subcategories = subcategories
            self.subcategory_combo.configure(values=subcategory_names)
            
            # Sélectionner la première sous-catégorie par défaut
            if subcategory_names:
                self.subcategory_combo.set(subcategory_names[0])
            else:
                self.subcategory_combo.set("")
    
    def validateForm(self) -> bool:
        """Valide le formulaire"""
        errors = []
        
        if not self.title_var.get().strip():
            errors.append("Le titre est obligatoire")
        
        if not self.date_var.get().strip():
            errors.append("La date est obligatoire")
        
        if not self.start_time_var.get().strip():
            errors.append("L'heure de début est obligatoire")
        
        if not self.end_time_var.get().strip():
            errors.append("L'heure de fin est obligatoire")
        
        if not self.category_combo.get():
            errors.append("La catégorie est obligatoire")
        
        # Validation du format de date
        try:
            datetime.strptime(self.date_var.get(), "%d/%m/%Y")
        except ValueError:
            errors.append("Format de date invalide (JJ/MM/AAAA)")
        
        # Validation des heures
        try:
            datetime.strptime(self.start_time_var.get(), "%H:%M")
            datetime.strptime(self.end_time_var.get(), "%H:%M")
        except ValueError:
            errors.append("Format d'heure invalide (HH:MM)")
        
        if errors:
            error_message = "\\n".join(errors)
            self.showError("Erreurs de validation", error_message)
            return False
        
        return True
    
    def save(self):
        """Sauvegarde le rendez-vous"""
        if not self.validateForm():
            return
        
        try:
            # Construire les données du rendez-vous
            appointment_data = self.buildAppointmentData()
            
            if self.is_editing:
                # Mise à jour
                success = self.updateAppointment(appointment_data)
                if success:
                    self.showSuccess("Rendez-vous modifié avec succès")
                else:
                    self.showError("Erreur", "Impossible de modifier le rendez-vous")
                    return
            else:
                # Création
                appointment_id = self.createAppointment(appointment_data)
                if appointment_id:
                    self.showSuccess("Rendez-vous créé avec succès")
                else:
                    self.showError("Erreur", "Impossible de créer le rendez-vous")
                    return
            
            # Appeler le callback si disponible
            if self.callback:
                self.callback(appointment_data)
            
            # Fermer le dialogue
            self.window.destroy()
            
        except Exception as e:
            self.showError("Erreur", f"Une erreur est survenue: {str(e)}")
    
    def buildAppointmentData(self) -> dict:
        """Construit les données du rendez-vous à partir du formulaire"""
        # Conversion de la date et heures
        appointment_date = datetime.strptime(self.date_var.get(), "%d/%m/%Y").date()
        start_time_obj = datetime.strptime(self.start_time_var.get(), "%H:%M").time()
        end_time_obj = datetime.strptime(self.end_time_var.get(), "%H:%M").time()
        
        start_datetime = datetime.combine(appointment_date, start_time_obj)
        end_datetime = datetime.combine(appointment_date, end_time_obj)
        
        # Récupérer les IDs de catégorie et sous-catégorie
        category = next((cat for cat in self.categories if cat.name == self.category_combo.get()), None)
        subcategory = None
        if self.subcategory_combo.get():
            subcategory = next((sub for sub in self.current_subcategories if sub.name == self.subcategory_combo.get()), None)
        
        return {
            'title': self.title_var.get().strip(),
            'description': self.description_textbox.get("1.0", "end-1c").strip(),
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'category_id': category.id if category else None,
            'subcategory_id': subcategory.id if subcategory else None
        }
    
    def createAppointment(self, data: dict) -> Optional[int]:
        """Crée un nouveau rendez-vous"""
        # Cette méthode devrait utiliser appointment_service
        # Pour l'instant, on retourne un ID fictif
        return 1
    
    def updateAppointment(self, data: dict) -> bool:
        """Met à jour un rendez-vous existant"""
        # Cette méthode devrait utiliser appointment_service
        # Pour l'instant, on retourne True
        return True
    
    def delete(self):
        """Supprime le rendez-vous (mode édition seulement)"""
        if not self.is_editing:
            return
        
        # Demander confirmation
        result = self.showConfirmation(
            "Confirmer la suppression",
            "Êtes-vous sûr de vouloir supprimer ce rendez-vous ?"
        )
        
        if result:
            # Supprimer le rendez-vous
            # success = appointment_service.deleteAppointment(self.appointment.id)
            success = True  # Simulé pour l'instant
            
            if success:
                self.showSuccess("Rendez-vous supprimé avec succès")
                if self.callback:
                    self.callback(None)  # Signal de suppression
                self.window.destroy()
            else:
                self.showError("Erreur", "Impossible de supprimer le rendez-vous")
    
    def cancel(self):
        """Annule et ferme le dialogue"""
        self.window.destroy()
    
    def showError(self, title: str, message: str):
        """Affiche un message d'erreur"""
        error_window = ctk.CTkToplevel(self.window)
        error_window.title(title)
        error_window.geometry("400x150")
        error_window.transient(self.window)
        error_window.grab_set()
        
        ctk.CTkLabel(error_window, text=message, wraplength=350).pack(pady=20)
        ctk.CTkButton(error_window, text="OK", command=error_window.destroy).pack(pady=10)
    
    def showSuccess(self, message: str):
        """Affiche un message de succès"""
        self.showError("Succès", message)
    
    def showConfirmation(self, title: str, message: str) -> bool:
        """Affiche une boîte de dialogue de confirmation"""
        # Implémentation simplifiée
        # Dans une vraie application, on utiliserait tkinter.messagebox
        return True