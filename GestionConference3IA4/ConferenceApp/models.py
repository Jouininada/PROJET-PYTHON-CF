from django.db import models                                       # permet de créer des modèles (tables)
from django.core.validators import MinLengthValidator, FileExtensionValidator  # valide la longueur et le type de fichier
from django.core.exceptions import ValidationError                 # permet de lever des erreurs de validation
import uuid                                                        # utilisé pour générer des identifiants uniques
from datetime import date                                          # utilisé pour comparer les dates


# =========================
# Modèle Conference
# =========================
class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)              # clé primaire auto-incrémentée
    name = models.CharField(max_length=255)                         # nom de la conférence
    description = models.TextField(validators=[                     # description avec validation
        MinLengthValidator(limit_value=30,                          # minimum 30 caractères
                           message="la description doit contenir au minimum 30 caractères")
    ])
    location = models.CharField(max_length=255)                     # lieu de la conférence

    # liste des thèmes possibles
    THEME = [
        ("CS&IA", "Computer science & IA"),
        ("CS", "Social science"),
        ("SE", "Science and eng")
    ]
    theme = models.CharField(max_length=255, choices=THEME)         # champ à choix limités
    start_date = models.DateField()                                 # date de début
    end_date = models.DateField()                                   # date de fin
    created_at = models.DateTimeField(auto_now_add=True)            # ajout automatique à la création
    updated_at = models.DateTimeField(auto_now=True)                # mise à jour automatique à chaque modification

    def clean(self):
        # vérifie que la date de début est avant la date de fin
        if self.start_date > self.end_date:
            raise ValidationError("la date de début de la conférence doit être antérieure à la date de fin")

    def __str__(self):
        # ce qui s’affiche dans l’admin ou en console
        return self.name


# =========================
# Fonctions utilitaires pour Submission
# =========================
def generate_submission_id():
    # génère un identifiant unique du type "SUBA1B2C3D4"
    return "SUB" + uuid.uuid4().hex[:8].upper()

def validate_keywords(value):
    # limite le nombre de mots-clés à 10 maximum
    keywords_list = [k.strip() for k in value.split(",")]
    if len(keywords_list) > 10:
        raise ValidationError("Vous ne pouvez pas avoir plus de 10 mots-clés (séparés par des virgules)")


# =========================
# Modèle Submission
# =========================
class Submission(models.Model):
    submission_id = models.CharField(primary_key=True, max_length=255, unique=True, editable=False)
    # identifiant unique non modifiable, généré automatiquement

    user = models.ForeignKey("UserApp.User",
                             on_delete=models.CASCADE,
                             related_name="submissions")
    # relie chaque soumission à un utilisateur (si supprimé → supprime aussi ses soumissions)

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="submissions")
    # relie chaque soumission à une conférence

    title = models.CharField(max_length=255)                        # titre de l’article
    abstract = models.TextField()                                   # résumé de l’article
    keywords = models.TextField(validators=[validate_keywords])     # liste de mots-clés (validée)
    paper = models.FileField(upload_to="papers/",
                             validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    # fichier PDF du papier soumis

    CHOICES = [                                                     # différents statuts possibles
        ("submitted", "submitted"),
        ("under review", "under review"),
        ("accepted", "accepted"),
        ("rejected", "rejected")
    ]
    status = models.CharField(max_length=255, choices=CHOICES)      # statut actuel
    payed = models.BooleanField(default=False)                      # indique si la soumission est payée
    submission_date = models.DateField(auto_now_add=True)           # date automatique à la création
    created_at = models.DateTimeField(auto_now_add=True)            # horodatage création
    updated_at = models.DateTimeField(auto_now=True)                # horodatage mise à jour

    def clean(self):
        # vérifie que la conférence n’est pas déjà passée
        if self.conference.start_date < date.today():
            raise ValidationError("Vous ne pouvez soumettre un article que pour une conférence à venir")

        # limite à 3 soumissions par utilisateur et par jour
        count_today = Submission.objects.filter(user=self.user,
                                                submission_date=date.today()).count()
        if self._state.adding and count_today >= 3:
            raise ValidationError("Vous ne pouvez soumettre plus de 3 articles par jour")

    def save(self, *args, **kwargs):
        # génère un ID unique seulement à la création
        if not self.submission_id:
            self.submission_id = generate_submission_id()
        super().save(*args, **kwargs)                               # sauvegarde classique du modèle

    def __str__(self):
        # affichage du titre + nom de l’utilisateur dans l’admin
        return f"{self.title} - {self.user.username}"
