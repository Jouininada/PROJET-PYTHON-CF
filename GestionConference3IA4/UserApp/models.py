from django.db import models  # Import des classes de base pour créer des modèles Django
from django.contrib.auth.models import AbstractUser  # Import pour créer un utilisateur personnalisé
from django.core.exceptions import ValidationError  # Pour lever des erreurs de validation
from django.core.validators import RegexValidator  # Pour valider le format de certains champs
import uuid  # Pour générer des identifiants uniques

# =========================
# Fonction pour générer un user_id unique
# =========================
def generate_userid():
    # Crée un identifiant unique de type 'USERXXXX' où XXXX sont des caractères hexadécimaux aléatoires
    return "USER" + uuid.uuid4().hex[:4].upper()

# =========================
# Fonction pour vérifier le domaine de l'email
# =========================
def verify_email(email):
    # Liste des domaines autorisés pour les emails universitaires privés
    domaine = ["esprit.tn", "seasame.com", "tek.tn", "central.com"]
    # Vérifie si le domaine de l'email est dans la liste
    if email.split("@")[1] not in domaine:
        # Si non, lève une erreur de validation
        raise ValidationError("l'email est invalide et doit appartenir à un domaine universitaire privé")

# =========================
# Regex pour valider les noms (lettres et espaces uniquement)
# =========================
name_validator = RegexValidator(
    regex=r'^[A-Za-z\s-]+$',  # Regex autorisant les lettres, espaces et tirets
    message="ce champ doit avoir des lettres et des espaces"  # Message affiché si non valide
)

# =========================
# Modèle User personnalisé
# =========================
class User(AbstractUser):
    user_id = models.CharField(
        max_length=8,  # Longueur maximale
        primary_key=True,  # Clé primaire
        unique=True,  # Doit être unique
        editable=False  # Non modifiable dans l'admin
    )
    first_name = models.CharField(
        max_length=100,
        validators=[name_validator]  # Valide le format du nom
    )
    last_name = models.CharField(
        max_length=100,
        validators=[name_validator]
    )
    email = models.EmailField(
        unique=True,  # Doit être unique
        validators=[verify_email]  # Valide le domaine
    )
    affiliation = models.CharField(max_length=255)  # Organisation ou université
    nationality = models.CharField(max_length=255)  # Nationalité
    ROLE = [
        ("Participant", "Participant"),
        ("commitee", "Organizing commitee member")  # Rôle dans le comité organisateur
    ]
    role = models.CharField(
        max_length=255,
        choices=ROLE,  # Limite les choix à la liste ROLE
        default="Participant"  # Valeur par défaut
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création automatique
    updated_at = models.DateTimeField(auto_now=True)  # Date de mise à jour automatique

    # =========================
    # Méthode save personnalisée
    # =========================
    def save(self, *args, **kwargs):
        # Si user_id n'est pas encore défini, on le génère
        if not self.user_id:
            new_id = generate_userid()
            # Vérifie que l'identifiant généré n'existe pas déjà
            while User.objects.filter(user_id=new_id).exists():
                new_id = generate_userid()
            self.user_id = new_id
        # Appelle la méthode save d'origine pour enregistrer l'objet
        super().save(*args, **kwargs)

    # Les relations ManyToMany commentées pour l'instant
    # submissions = models.ManyToManyField("ConferenceApp.Conference", through="Submission")
    # organizingCommiteeList = models.ManyToManyField("ConferenceApp.Conference", through="OrganizingCommitee")


# =========================
# Modèle OrganizingCommitee
# =========================
class OrganizingCommitee(models.Model):
    # Lien vers l'utilisateur qui fait partie du comité
    user = models.ForeignKey(
        "UserApp.User",  # Référence le modèle User dans l'app UserApp
        on_delete=models.CASCADE,  # Si l'utilisateur est supprimé, le comité aussi
        related_name="commitees"  # Nom utilisé pour accéder aux comités depuis User
    )
    # Lien vers la conférence
    conference = models.ForeignKey(
        "ConferenceApp.Conference",  # Référence le modèle Conference
        on_delete=models.CASCADE,
        related_name="commitees"
    )
    ROLES = [
        ("chair", "chair"),  # Président
        ("co-chair", "co-chair"),  # Co-président
        ("member", "member")  # Membre simple
    ]
    commitee_role = models.CharField(
        max_length=255,
        choices=ROLES  # Limite les choix au rôle défini
    )
    date_join = models.DateField()  # Date d'adhésion au comité
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    updated_at = models.DateTimeField(auto_now=True)  # Date de mise à jour
