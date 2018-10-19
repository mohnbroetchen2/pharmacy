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
from .models import Product, Pharmacy, Person, Submission, DrugClass, Company, Submission
from .filters import ProductFilter
from django.utils.html import strip_tags

@login_required
def start_view(request):
    productlist = Product.objects.all()
    f = ProductFilter(request.GET, queryset=productlist)
    return render(request, 'home.html', {'filter': f})

@login_required
def submit_view(request, primary_key):
    product= get_object_or_404(Product, pk=primary_key)
    persons = Person.objects.filter(state='active')
    available_containers = product.available_containers()
    available_quantity = product.available_quantity()
    available_quantity_last_container = product.available_quantity_last_container()
    return render(request, 'submit.html', {'object': product, 'persons':persons, 'range':range(available_containers-1), 'quantity_last_container':available_quantity_last_container,})

@login_required
def createsubmission(request):
    if request.method == "POST":
        productid = request.POST.get("productid")
        personid  = request.POST.get("recipient")
        new_submission = Submission();
        new_submission.product              = Product.objects.get(pk=productid)
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
    product= get_object_or_404(Product, pk=primary_key)
    submissionlist = Submission.objects.filter(product__pk=primary_key).order_by('-date')
    available_containers = product.available_containers()
    available_quantity = product.available_quantity()
    available_quantity_last_container = product.available_quantity_last_container()
    return render(request, 'submissions.html', {'product': product, 'submissions':submissionlist, 'range':range(available_containers-1), 'quantity_last_container':available_quantity_last_container,})
