from django.db import models  # Pour créer des modèles Django (tables dans la BDD)
from django.core.validators import RegexValidator  # Pour valider certains formats de texte
from django.core.exceptions import ValidationError  # Pour lever des erreurs si une validation échoue

# =========================
# Validators (fonctions pour vérifier certaines règles)
# =========================

# Vérifie que le nom de la salle contient uniquement lettres, chiffres et espaces
room_validator = RegexValidator(
    regex=r'^[A-Za-z0-9\s]+$',  # Regex : lettres A-Z, a-z, chiffres 0-9 et espaces
    message="Le nom de la salle ne doit contenir que des lettres et des chiffres"  
)

# Vérifie que la date de la session est bien dans la période de la conférence
def validate_session_day(session_day, conference):
    """
    session_day : date de la session
    conference : objet Conference
    """
    if session_day < conference.start_date or session_day > conference.end_date:
        raise ValidationError("La date de la session doit être comprise entre la date de début et de fin de la conférence")

# Vérifie que l'heure de fin est après l'heure de début
def validate_start_end_time(start_time, end_time):
    if end_time <= start_time:
        raise ValidationError("L'heure de fin doit être supérieure à l'heure de début")

# =========================
# Modèle Session (table pour stocker les sessions de conférences)
# =========================
class Session(models.Model):
    session_id = models.AutoField(primary_key=True)  
    # ID unique de la session, auto-incrémenté

    title = models.CharField(max_length=255)  
    # Titre de la session

    topic = models.CharField(max_length=255)  
    # Sujet / thème de la session

    session_day = models.DateField()  
    # Date à laquelle la session a lieu

    start_time = models.TimeField()  
    # Heure de début

    end_time = models.TimeField()  
    # Heure de fin

    room = models.CharField(max_length=255, validators=[room_validator])  
    # Nom de la salle avec validation (lettres/chiffres seulement)

    created_at = models.DateTimeField(auto_now_add=True)  
    # Date de création automatique

    updated_at = models.DateTimeField(auto_now=True)  
    # Date de mise à jour automatique

    conference = models.ForeignKey(
        "ConferenceApp.Conference",  # Lien vers la conférence correspondante
        on_delete=models.CASCADE,    # Si la conférence est supprimée, ses sessions le seront aussi
        related_name="sessions"      # Permet de récupérer toutes les sessions d’une conférence via conference.sessions
    )

    # =========================
    # Validation personnalisée avant sauvegarde
    # =========================
    def clean(self):
        """
        Fonction qui valide certaines règles avant d'enregistrer la session
        """
        # Vérifie que la date de la session est dans la période de la conférence
        if self.conference:
            validate_session_day(self.session_day, self.conference)

        # Vérifie que l'heure de fin est après l'heure de début
        validate_start_end_time(self.start_time, self.end_time)

    # =========================
    # Représentation lisible d'une session
    # =========================
    def __str__(self):
        return f"{self.title} ({self.session_day}) - {self.conference.name}"
        # Exemple affichage : "Introduction à l'IA (2025-10-20) - Conférence CS&IA"
