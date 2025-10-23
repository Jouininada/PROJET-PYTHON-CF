from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView,DetailView
# Create your views here.

def all_conference(req):
    conferences=Conference.objects.all()
    return render(req,'conference/listConference.html',{'conferences':conferences})
# Create your views here.

#hne lezmk t7out nafs l esm     context_object_name="conferences"

class ConferenceList(ListView):
    model= Conference
    context_object_name="conferences"
    ordering=['start_date']
    template_name='conference/listConference.html'

class ConferenceDetails(DetailView):
     model= Conference
     context_object_name="conference"
     template_name='conference/listConference.html'