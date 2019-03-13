from django.http import HttpResponse
from .models import Change
from django.shortcuts import render
from .filters import ChangeFilter

def changehistory(request):
    changelist = Change.objects.all()
    f = ChangeFilter(request.GET, queryset=changelist)
    return render(request, 'changes.html', {'filter': f})
