from django.contrib import admin
from .models import User, OrganizingCommitee

# =========================
# 🎨 Personnalisation du tableau de bord admin
# =========================
admin.site.site_header = "Conference Management Admin"      # Titre principal de la page admin
admin.site.site_title = "Conference Dashboard"               # Titre affiché dans l’onglet du navigateur
admin.site.index_title = "Gestion des utilisateurs et comités"  # Titre de la page d’accueil de l’admin


# =========================
# 👤 Admin pour le modèle User
# =========================
@admin.register(User)  # Enregistre le modèle User dans l’interface admin
class UserAdmin(admin.ModelAdmin):

    # Colonnes visibles dans la liste des utilisateurs
    list_display = ("user_id", "username", "first_name", "last_name", "email",
                    "role", "affiliation", "nationality", "created_at")
    # → permet d’afficher les infos principales de chaque utilisateur

    # Champs modifiables directement dans la liste
    list_editable = ("role", "affiliation", "nationality")
    # → permet de modifier ces valeurs sans ouvrir la fiche de l’utilisateur

    # Filtres affichés sur le côté
    list_filter = ("role", "affiliation", "nationality", "date_joined")
    # → permet de filtrer les utilisateurs par rôle, pays, affiliation, ou date d’inscription

    # Barre de recherche
    search_fields = ("username", "first_name", "last_name", "email")
    # → permet de chercher un utilisateur par son nom ou email

    # Organisation du formulaire d’édition
    fieldsets = (
        ("Identité", {
            "fields": ("user_id", "username", "first_name", "last_name", "email")
        }),
        ("Informations supplémentaires", {
            "fields": ("affiliation", "nationality", "role")
        }),
        ("Dates", {
            "fields": ("date_joined", "last_login", "created_at", "updated_at")
        }),
    )
    # → regroupe les champs par catégorie pour un formulaire plus clair

    # Champs en lecture seule
    readonly_fields = ("user_id", "date_joined", "created_at", "updated_at", "last_login")
    # → empêche la modification manuelle de ces champs gérés automatiquement


# =========================
# 🧑‍💼 Admin pour le modèle OrganizingCommitee
# =========================
@admin.register(OrganizingCommitee)  # Enregistre le modèle dans l’admin
class OrganizingCommiteeAdmin(admin.ModelAdmin):

    # Colonnes visibles dans la liste
    list_display = ("user", "conference", "commitee_role", "date_join", "created_at")
    # → montre les infos principales de chaque membre du comité

    # Filtres sur le côté
    list_filter = ("commitee_role", "conference", "date_join")
    # → permet de filtrer les membres selon leur rôle, conférence ou date d’ajout

    # Barre de recherche
    search_fields = ("user__username", "conference__name")
    # → permet de rechercher par nom d’utilisateur ou par nom de conférence
    # (le double underscore "__" permet d’accéder à un champ d’un modèle lié)

    # Organisation du formulaire
    fieldsets = (
        ("Informations générales", {
            "fields": ("user", "conference", "commitee_role")
        }),
        ("Dates", {
            "fields": ("date_join", "created_at", "updated_at")
        }),
    )
    # → structure le formulaire d’édition en deux parties : infos et dates

    # Champs non modifiables
    readonly_fields = ("created_at", "updated_at")
    # → empêche de modifier les champs automatiques
