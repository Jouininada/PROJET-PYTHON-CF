from django.urls import path
from .views import ConferenceList  # ✅ Import direct de la classe

urlpatterns = [
    # path("liste/", views.all_conference, name='all_conference'),  # ancienne version (FBV)
    path("liste/", ConferenceList.as_view(), name='conference_list'),  # nouvelle version (CBV)
]
