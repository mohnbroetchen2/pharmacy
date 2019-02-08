from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from .models import Pharmacy, Person, Submission, DrugClass, Company, StockProduct
from .filters import StockProductFilter, PharmacyFilter
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect

@login_required
def start_view(request):
    pharmacylist = Pharmacy.objects.all()
    i=0
    #for p in pharmacylist:
        #if p.available_quantity() == 0:
        #    pharmacylist.delete(i)
        #    i=i+1
    f = PharmacyFilter(request.GET, queryset=pharmacylist)
    return render(request, 'home.html', {'filter': f})

def active_pharmacy_view(request, primary_key):
    pharmacy = Pharmacy.objects.get(pk=primary_key)
    stockProductlist =  StockProduct.object.filter(pharmacy__pk=primary_key).filter(state='active')
    return render(request, 'home.html', {'filter': f})

@login_required
def submit_view(request, primary_key):
    product= get_object_or_404(StockProduct, pk=primary_key)
    persons = Person.objects.filter(state='active')
    available_containers = product.available_containers()
    available_quantity = product.available_quantity()
    available_quantity_last_container = product.available_quantity_last_container()
    return render(request, 'submit.html', {'object': product, 'persons':persons, 'range':range(int(available_containers)-1), 'quantity_last_container':available_quantity_last_container,})

@login_required
def createsubmission(request):
    if request.method == "POST":
        productid = request.POST.get("productid")
        personid  = request.POST.get("recipient")
        new_submission = Submission();
        new_submission.product              = StockProduct.objects.get(pk=productid)
        new_submission.person               = Person.objects.get(pk=personid)
        new_submission.application_number   = request.POST.get("application_number",None)
        new_submission.date                 = request.POST.get("submission_date",None)
        new_submission.amount_containers    = request.POST.get("full_containers",0)
        new_submission.quantity             = request.POST.get("quantity",0)
        new_submission.comment              = request.POST.get("comment",None)
        new_submission.added_by             = request.user
        new_submission.save()
        messages.add_message(request, messages.SUCCESS, 'Submission with id {} saved'.format(new_submission.pk))
        return HttpResponseRedirect('/')

@login_required
def seesubmissions(request, primary_key):
    # übergabe der arznei --> Anzeige aller aktiven produkte mit deren submissions
    #pharmacy = Pharmacy.objects.get(pk=primary_key)
    #oder
    productlist = StockProduct.objects.filter(state='active').filter(pharmacy__pk=primary_key)
    
    #product= get_object_or_404(StockProduct, pk=primary_key)
    #submissionlist = Submission.objects.filter(product__pk=primary_key).order_by('-date')
    #available_containers = product.available_containers()
    #available_quantity = product.available_quantity()
    #available_quantity_last_container = product.available_quantity_last_container()
    return render(request, 'submissions.html', {'product': product, 'submissions':submissionlist, 'quantity_last_container':available_quantity_last_container,})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
