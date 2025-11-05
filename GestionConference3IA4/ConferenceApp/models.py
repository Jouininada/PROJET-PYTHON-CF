from django.db import models
from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
import uuid
from datetime import date


# =========================
# Modèle Conference
# =========================
class Conference(models.Model):
    conference_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(validators=[
        MinLengthValidator(limit_value=30,
                           message="la description doit contenir au minimum 30 caractères")
    ])
    location = models.CharField(max_length=255)
    THEME = [
        ("CS&IA", "Computer science & IA"),
        ("CS", "Social science"),
        ("SE", "Science and eng")
    ]
    theme = models.CharField(max_length=255, choices=THEME)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError("la date de début de la conférence doit être antérieure à la date de fin")

    def __str__(self):
        return self.name


# =========================
# Fonctions utilitaires pour Submission
# =========================
def generate_submission_id():
    return "SUB" + uuid.uuid4().hex[:8].upper()


def validate_keywords(value):
    keywords_list = [k.strip() for k in value.split(",")]
    if len(keywords_list) > 10:
        raise ValidationError("Vous ne pouvez pas avoir plus de 10 mots-clés (séparés par des virgules)")


# =========================
# Modèle Submission
# =========================
class Submission(models.Model):
    submission_id = models.CharField(primary_key=True, max_length=255, unique=True, editable=False)
    user = models.ForeignKey("UserApp.User", on_delete=models.CASCADE, related_name="submissions")
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="submissions")
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    keywords = models.TextField(validators=[validate_keywords])
    paper = models.FileField(upload_to="papers/", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    CHOICES = [
        ("submitted", "submitted"),
        ("under review", "under review"),
        ("accepted", "accepted"),
        ("rejected", "rejected")
    ]
    status = models.CharField(max_length=255, choices=CHOICES)
    payed = models.BooleanField(default=False)
    submission_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.conference and self.conference.start_date:
            if self.conference.start_date < date.today():
                raise ValidationError("Vous ne pouvez soumettre un article que pour une conférence à venir")

        count_today = Submission.objects.filter(user=self.user,
                                                submission_date=date.today()).count()
        if self._state.adding and count_today >= 3:
            raise ValidationError("Vous ne pouvez soumettre plus de 3 articles par jour")

    def save(self, *args, **kwargs):
        if not self.submission_id:
            self.submission_id = generate_submission_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
