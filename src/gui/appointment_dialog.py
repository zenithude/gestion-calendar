"""Dialogue pour créer/éditer des rendez-vous"""

import customtkinter as ctk
from datetime import datetime, date, time
from typing import Optional, Callable, List
from src.services.category_service import CategoryService
from src.models.appointment import Appointment
from src.models.category import Category
from src.models.subcategory import Subcategory
from src.utils.theme import getButtonStyle, getFrameStyle, SIZES, COLORS, FONTS


class AppointmentDialog:
    """Dialogue pour la création et modification de rendez-vous"""
    
    def __init__(self, parent, category_service: CategoryService, 
                 appointment_service, appointment: Optional[Appointment] = None, 
                 callback: Optional[Callable] = None):
        self.parent = parent
        self.category_service = category_service
        self.appointment_service = appointment_service
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
        self.window.geometry(f"{SIZES['dialog_width']}x{SIZES['dialog_height']}")
        self.window.resizable(True, True)
        self.window.transient(self.parent)
        
        # Afficher l'interface d'abord
        self.setupUI()
        self.loadData()
        
        # Centrer la fenêtre après création du contenu
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (SIZES['dialog_width'] // 2)
        y = (self.window.winfo_screenheight() // 2) - (SIZES['dialog_height'] // 2)
        self.window.geometry(f"{SIZES['dialog_width']}x{SIZES['dialog_height']}+{x}+{y}")
        
        # Forcer l'affichage complet avant grab_set
        self.window.update()
        
        # Différer le grab_set pour être sûr que la fenêtre est visible
        self.window.after(100, self._setWindowFocus)
    
    def _setWindowFocus(self):
        """Configure le focus de la fenêtre de manière sécurisée"""
        try:
            if self.window and self.window.winfo_exists():
                self.window.grab_set()
                self.window.focus_set()
                self.window.lift()  # Amener au premier plan
        except Exception as e:
            print(f"Info: Focus automatique indisponible: {e}")
    
    def _setPopupFocus(self, popup_window):
        """Configure le focus d'une fenêtre popup de manière sécurisée"""
        try:
            if popup_window and popup_window.winfo_exists():
                popup_window.grab_set()
                popup_window.focus_set()
                popup_window.lift()
        except Exception as e:
            print(f"Info: Focus popup indisponible: {e}")
    
    def setupUI(self):
        """Configure l'interface du dialogue"""
        # Frame principal avec style
        main_frame_style = getFrameStyle("dialog")
        main_frame = ctk.CTkFrame(self.window, **main_frame_style)
        main_frame.pack(fill="both", expand=True, padx=SIZES["spacing_xl"], pady=SIZES["spacing_xl"])
        
        # Titre avec style amélioré
        title_label = ctk.CTkLabel(
            main_frame,
            text="Modifier le rendez-vous" if self.is_editing else "Créer un nouveau rendez-vous",
            font=ctk.CTkFont(size=FONTS["size_title"], weight=FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title_label.pack(pady=(SIZES["spacing_md"], SIZES["spacing_xl"]))
        
        # Formulaire avec style
        form_frame_style = getFrameStyle("card")
        form_frame = ctk.CTkFrame(main_frame, **form_frame_style)
        form_frame.pack(fill="both", expand=True, padx=SIZES["spacing_md"], pady=(0, SIZES["spacing_md"]))
        
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
        
        # Boutons d'action avec styles appropriés
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(SIZES["spacing_md"], 0))
        
        # Bouton Annuler
        cancel_btn_style = getButtonStyle("secondary")
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Annuler",
            command=self.cancel,
            **cancel_btn_style
        )
        cancel_btn.pack(side="right", padx=(SIZES["spacing_md"], 0))
        
        # Bouton Sauvegarder/Modifier
        save_btn_style = getButtonStyle("primary")
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Modifier" if self.is_editing else "Créer",
            command=self.save,
            **save_btn_style
        )
        save_btn.pack(side="right")
        
        # Bouton supprimer (seulement en mode édition)
        if self.is_editing:
            delete_btn_style = getButtonStyle("error")
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="Supprimer",
                command=self.delete,
                **delete_btn_style
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
        try:
            appointment_id = self.appointment_service.createAppointment(
                title=data['title'],
                description=data['description'],
                start_datetime=data['start_datetime'],
                end_datetime=data['end_datetime'],
                category_id=data['category_id'],
                subcategory_id=data['subcategory_id']
            )
            return appointment_id
        except Exception as e:
            print(f"Erreur lors de la création du rendez-vous: {e}")
            return None
    
    def updateAppointment(self, data: dict) -> bool:
        """Met à jour un rendez-vous existant"""
        try:
            success = self.appointment_service.updateAppointment(
                appointment_id=self.appointment.id,
                title=data['title'],
                description=data['description'],
                start_datetime=data['start_datetime'],
                end_datetime=data['end_datetime'],
                category_id=data['category_id'],
                subcategory_id=data['subcategory_id']
            )
            return success
        except Exception as e:
            print(f"Erreur lors de la mise à jour du rendez-vous: {e}")
            return False
    
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
            try:
                success = self.appointment_service.deleteAppointment(self.appointment.id)
                
                if success:
                    self.showSuccess("Rendez-vous supprimé avec succès")
                    if self.callback:
                        self.callback(None)  # Signal de suppression
                    self.window.destroy()
                else:
                    self.showError("Erreur", "Impossible de supprimer le rendez-vous")
            except Exception as e:
                self.showError("Erreur", f"Erreur lors de la suppression: {e}")
    
    def cancel(self):
        """Annule et ferme le dialogue"""
        self.window.destroy()
    
    def showError(self, title: str, message: str):
        """Affiche un message d'erreur"""
        error_window = ctk.CTkToplevel(self.window)
        error_window.title(title)
        error_window.geometry("400x150")
        error_window.transient(self.window)
        
        # Contenu du dialogue
        ctk.CTkLabel(error_window, text=message, wraplength=350).pack(pady=20)
        ctk.CTkButton(error_window, text="OK", command=error_window.destroy).pack(pady=10)
        
        # Centrer la fenêtre
        error_window.update_idletasks()
        x = error_window.winfo_x() + (error_window.winfo_width() // 2) - 200
        y = error_window.winfo_y() + (error_window.winfo_height() // 2) - 75
        error_window.geometry(f"400x150+{x}+{y}")
        
        # Focus sécurisé différé
        error_window.after(50, lambda: self._setPopupFocus(error_window))
    
    def showSuccess(self, message: str):
        """Affiche un message de succès"""
        self.showError("Succès", message)
    
    def showConfirmation(self, title: str, message: str) -> bool:
        """Affiche une boîte de dialogue de confirmation"""
        # Implémentation simplifiée
        # Dans une vraie application, on utiliserait tkinter.messagebox
        return True