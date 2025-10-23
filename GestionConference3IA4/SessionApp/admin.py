from django.contrib import admin
from .models import Session

# =========================
# Personnalisation de l'admin pour Session
# =========================
@admin.register(Session)  # Enregistre le modèle Session dans l’interface admin
class SessionAdmin(admin.ModelAdmin):

    # Colonnes affichées dans la liste admin
    list_display = ("session_id", "title", "topic", "conference", "session_day", "start_time", "end_time", "room", "created_at")
    # → permet d’afficher ces infos dans le tableau principal

    # Champs modifiables directement dans la liste
    list_editable = ("start_time", "end_time", "room")
    # → permet de changer ces valeurs sans ouvrir la fiche

    # Filtres affichés sur le côté
    list_filter = ("conference", "session_day", "room", "topic")
    # → permet de filtrer les sessions selon ces critères

    # Barre de recherche
    search_fields = ("title", "topic", "room", "conference__name")
    # → permet de chercher une session par titre, thème, salle ou nom de conférence

    # Organisation du formulaire d’édition
    fieldsets = (
        ("Informations générales", { "fields": ("title", "topic", "conference", "room") }),
        ("Horaires", { "fields": ("session_day", "start_time", "end_time") }),
        ("Dates de suivi", { "fields": ("created_at", "updated_at") }),
    )
    # → regroupe les champs par section pour un affichage plus clair

    # Champs en lecture seule
    readonly_fields = ("created_at", "updated_at")
    # → empêche la modification manuelle de ces champs
