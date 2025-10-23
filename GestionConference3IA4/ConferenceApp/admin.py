from django.contrib import admin        # pour pouvoir utiliser admin.site et les ModelAdmin
from .models import Conference, Submission  # pour accéder à tes modèles


# =========================
# Personnalisation du tableau de bord admin
# =========================
admin.site.site_header = "Conference Management admin 25/26"   # Titre affiché en haut du site admin
admin.site.site_title = "Conference dashboard"                 # Titre dans l’onglet du navigateur
admin.site.index_title = "Conference management"               # Titre de la page d’accueil de l’admin


# Inlines pour Submission (affichage des soumissions liées à une conférence)

class SubmissionStackedInline(admin.StackedInline):
    """
    Affiche les soumissions sous forme de formulaire vertical (stacked)
    directement dans la page d’une conférence.
    """
    model = Submission                                          # Le modèle associé
    extra = 1                                                   # Nombre de lignes vides supplémentaires
    readonly_fields = ("submission_id", "submission_date")      # Champs non modifiables dans l’admin


class SubmissionTabularInline(admin.TabularInline):
    """
    Même concept que StackedInline mais avec un affichage en tableau (plus compact).
    """
    model = Submission
    extra = 1
    readonly_fields = ("submission_id", "submission_date")      # Ces champs ne sont pas éditables
    fields = ("title", "status", "user", "payed")               # Champs visibles dans l’inline


# Personnalisation de l’admin pour le modèle Conference

@admin.register(Conference)
class AdminPerso(admin.ModelAdmin):
    """
    Configuration de l’interface admin pour les conférences.
    """
    # Colonnes affichées dans la liste principale
    list_display = ("name", "theme", "location", "start_date", "end_date", "duration")

    # Tri par date de début
    ordering = ("start_date",)

    # Filtres rapides sur le côté
    list_filter = ("theme", "location", "start_date")

    # Barre de recherche
    search_fields = ("name", "description", "location")

    # Organisation du formulaire d’édition
    fieldsets = (
        ("Informations générales", {
            "fields": ("conference_id", "name", "theme", "description")
        }),
        ("Logistique", {
            "fields": ("location", "start_date", "end_date")
        }),
    )

    # Champs non modifiables
    readonly_fields = ("conference_id",)

    # Ajoute une barre de navigation temporelle par date de début
    date_hierarchy = "start_date"

    # Affiche les soumissions associées sous chaque conférence
    inlines = [SubmissionStackedInline]

    def duration(self, obj):
        """
        Calcule la durée (en jours) d’une conférence à partir des dates.
        """
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return "RAS"  # Si les dates sont manquantes
    duration.short_description = "Durée (jours)"


# Personnalisation de l’admin pour le modèle Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """
    Configuration de l’interface admin pour les soumissions.
    """
    # Colonnes visibles dans la liste
    list_display = ("title", "status", "user", "conference", "submission_date", "payed", "short_abstract")

    # Champs modifiables directement depuis la liste
    list_editable = ("status", "payed")

    # Filtres latéraux pour affiner la recherche
    list_filter = ("status", "payed", "conference", "submission_date")

    # Barre de recherche
    search_fields = ("title", "keywords", "user__username")

    # Organisation du formulaire d’édition
    fieldsets = (
        ("Informations générales", {
            "fields": ("submission_id", "title", "abstract", "keywords")
        }),
        ("Fichier et conférence associée", {
            "fields": ("paper", "conference")
        }),
        ("Suivi et état", {
            "fields": ("status", "payed", "submission_date", "user")
        }),
    )

    # Champs non modifiables
    readonly_fields = ("submission_id", "submission_date")

    def short_abstract(self, obj):
        """
        Retourne uniquement les 50 premiers caractères du résumé
        pour un affichage compact dans la liste admin.
        """
        return obj.abstract[:50] + ("..." if len(obj.abstract) > 50 else "")
    short_abstract.short_description = "Résumé (court)"


    # Actions personnalisées dans le menu déroulant admin


    actions = ["mark_as_payed", "accept_submissions"]

    def mark_as_payed(self, request, queryset):
        """
        Action : marque les soumissions sélectionnées comme payées.
        """
        updated = queryset.update(payed=True)
        self.message_user(request, f"{updated} soumission(s) marquée(s) comme payée(s).")
    mark_as_payed.short_description = "Marquer comme payées"

    def accept_submissions(self, request, queryset):
        """
        Action : marque les soumissions sélectionnées comme 'acceptées'.
        """
        updated = queryset.update(status="accepted")
        self.message_user(request, f"{updated} soumission(s) acceptée(s).")
    accept_submissions.short_description = "Accepter les soumissions"


    
