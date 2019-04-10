from django.shortcuts import render
from django.views import generic
from datetime import datetime
from django import forms
import time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from .models import Pharmacy, Person, Submission, DrugClass, Company, Order
from .filters import OrderFilter, PharmacyFilter, SubmissionFilter
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
import csv
import codecs
from .forms import addOrderForm
from django.core.mail import send_mail


#view is responsible for one form: when form is first initiated (else) and when the form is submitted  with data (if)
def add_order(request):
    try:
        if request.method == 'POST':  # If the form has been submitted...
            form = addOrderForm(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                pharmacy = Pharmacy.objects.all()
                new_order = Order()
                new_order.pharmacy = pharmacy[int(request.POST['pharmacy'])-2] #doesnt work
                new_order.state = request.POST['state']  # == 0 ? 'active' : 'deactivated' #is ok
                new_order.amount_containers = request.POST['amount']
                new_order.quantity = request.POST['quantity']
                new_order.unit = request.POST['unit']
                new_order.delivery_date = "2017-05-22"
                #new_order.delivery_date = request.POST['delivery'] #doesnt work
                #new_order.expiry_date = request.POST['expiry'] #doesnt work
                new_order.batch_number = request.POST['batch']
                new_order.comment = request.POST['comment']
                new_order.added_by = request.user
                #new_order.save() #doesnt work

                return HttpResponseRedirect('/')  # Redirect after POST
        else:
            return render(request, 'form_orderadd.html', {'form': addOrderForm()})
    except:
        print("error")

@login_required
def exportcsvadvanced(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="FLI_pharmacy.csv"'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=',', dialect='excel')
    pharmacy = Pharmacy.objects.all()

#get the dates the user has chosen for the export
    fromDate = request.POST.get("exportFromDate", None)
    toDate = request.POST.get("exportToDate", None)

#write the csv file
    #write the header
    writer.writerow(
        ["Name", "Molecule", "Start Quantity", "End Quantity", "Start Date", "End Date", "Company", "State", "Drug Class", "Dose", "Type", "Animal Species", "Umwidmungsstufe",
         'application_number', 'order', 'person', 'date', 'amount_containers', 'quantity', 'total quantity', 'comment', 'procedure_control'])
    #for each pharmacy, write the following lines
    for p in pharmacy:
        #each pharmacy is listed
        writer.writerow([p.name, p.get_molecule(),
                         "{} {}".format(p.available_quantity_date(Date=datetime.date(datetime.strptime(toDate, '%Y-%m-%d'))), p.unit()), #to- and from-date have to be reversed here, but I don't know why
                         "{} {}".format(p.available_quantity_date(Date=datetime.date(datetime.strptime(fromDate, '%Y-%m-%d'))), p.unit()),
                         datetime.date(datetime.strptime(fromDate, '%Y-%m-%d')), datetime.date(datetime.strptime(toDate, '%Y-%m-%d')),
                         p.company, p.state, p.get_drug_class(), p.dose, p.type, p.animal_species, p.umwidmungsstufe])
    for p in pharmacy:
        # each submussion (of each pharmacy) has a row
        submissionlist = Submission.objects.filter(order__pharmacy__pk=p.pk)
        for s in submissionlist:
            if (s.date >= datetime.date(datetime.strptime(fromDate, '%Y-%m-%d'))) & \
                    (s.date <= datetime.date(datetime.strptime(toDate, '%Y-%m-%d'))):
                writer.writerow(
                    [p.name, p.get_molecule(),
                     "{} {}".format(p.available_quantity_date(Date=datetime.date(datetime.strptime(toDate, '%Y-%m-%d'))), p.unit()),
                     "{} {}".format(p.available_quantity_date(Date=datetime.date(datetime.strptime(fromDate, '%Y-%m-%d'))), p.unit()),
                     datetime.date(datetime.strptime(fromDate, '%Y-%m-%d')),
                     datetime.date(datetime.strptime(toDate, '%Y-%m-%d')),
                     p.company, p.state, p.get_drug_class(), p.dose, p.type, p.animal_species, p.umwidmungsstufe,
                     s.application_number, s.order, s.person, s.date,
                    s.amount_containers,
                     "{} {}".format(s.quantity, p.unit()),
                     "{} {}".format(s.fullamount(), p.unit()),
                     s.comment, s.procedure_control])
    return response

@login_required #used to export items, that have a quantity higher than 0 (used in Home)
def exportcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="FLI_pharmacy.csv"'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=',', dialect='excel')
    pharmacy = Pharmacy.objects.all()
    writer.writerow(["Name", "Molecule","available Quantity", "available Container", "Company", "State", "Drug Class", "Dose", "Type", "Animal Species", "Umwidmungsstufe", "Storage Instructions",
                    "Comment"])
    for p in pharmacy:
        if p.available_quantity()>0:
            writer.writerow([p.name, p.get_molecule(),"{}{}".format(p.available_quantity(), p.unit()), p.available_container(), p.company, p.state, p.get_drug_class(), p.dose,
                             p.type, p.animal_species, p.umwidmungsstufe, p.storage_instructions, p.comment])
    return response

@login_required #used to export all items, independent of their quantity (used in Full Overview)
def exportcsv_all(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="FLI_pharmacy.csv"'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=',', dialect='excel')
    pharmacy = Pharmacy.objects.all()
    writer.writerow(["Name", "Molecule","available Quantity", "available Container", "Company", "State", "Drug Class", "Dose", "Type", "Animal Species", "Umwidmungsstufe", "Storage Instructions",
                    "Comment"])
    for p in pharmacy:
        writer.writerow([p.name, p.get_molecule(),"{}{}".format(p.available_quantity(), p.unit()), p.available_container(), p.company, p.state, p.get_drug_class(), p.dose,
                         p.type, p.animal_species, p.umwidmungsstufe, p.storage_instructions, p.comment])
    return response

@login_required
def start_view(request):
    pharmacylist = Pharmacy.objects.all()
    #i=0
    #for p in pharmacylist:
    #    if p.available_quantity() == 0:
     #      pharmacylist.remove(i)
     #   i=i+1
    f = PharmacyFilter(request.GET, queryset=pharmacylist)
    return render(request, 'home.html', {'filter': f})

@login_required
def active_pharmacy_view(request, primary_key):
    pharmacy = Pharmacy.objects.get(pk=primary_key)
    orderlist =  Order.object.filter(pharmacy__pk=primary_key).filter(state='active')
    return render(request, 'home.html', {'filter': f})

@login_required
def start_all_view(request):
    pharmacylist = Pharmacy.objects.all()
    f = PharmacyFilter(request.GET, queryset=pharmacylist)
    return render(request, 'home_all.html', {'filter': f})

@login_required
def submit_view(request, primary_key):
    if primary_key == 0:
        if request.method == "POST":
            pk_order = request.POST.get("selected",None)
            if pk_order:
                primary_key = pk_order
    order= get_object_or_404(Order, pk=primary_key)
    persons = Person.objects.filter(state='active')
    available_containers = order.available_containers()
    available_quantity = order.available_quantity()
    available_quantity_last_container = order.available_quantity_last_container()
    return render(request, 'submit.html', {'object': order, 'persons':persons, 'range':range(int(available_containers)-1), 'quantity_last_container':available_quantity_last_container,'available_containers':available_containers,})

@login_required
def selectpharmacyforsubmitview(request, primary_key):
    order = Order.objects.filter(pharmacy__pk=primary_key).filter(state='active')
    pharmacy = get_object_or_404(Pharmacy, pk=primary_key)
    if len(order) > 1:
        return render(request, 'selectpharmacyforsubmit.html', {'order': order, 'pharmacy': pharmacy,})
    else:
        return(submit_view(request,order[0].pk))


@login_required
def createsubmission(request):
    if request.method == "POST":
        productid = request.POST.get("productid")
        personid  = request.POST.get("recipient")

        orderObject = Order.objects.get(pk=productid)
        pharmacyObject = orderObject.pharmacy

        new_submission = Submission();
        new_submission.order                = orderObject
        new_submission.person               = Person.objects.get(pk=personid)
        new_submission.application_number   = request.POST.get("application_number",None)
        new_submission.date                 = request.POST.get("submission_date",None)
        new_submission.amount_containers    = request.POST.get("full_containers",0)
        new_submission.quantity             = request.POST.get("quantity",0)
        new_submission.comment              = request.POST.get("comment",None)
        new_submission.added_by             = request.user
        new_submission.save()
        messages.add_message(request, messages.SUCCESS, 'Submission with id {} saved'.format(new_submission.pk))


        quantityMin = pharmacyObject.alarm_value
        quantityCurrent = pharmacyObject.available_quantity() #is this the total quantity?yes
        quantitySubmission = float(request.POST.get("full_containers",0)) * float(orderObject.quantity) + float(request.POST.get("quantity",0))

        if (quantitySubmission>=(quantityCurrent-quantityMin)):
            # from_email = "bushaltestelle.80@web.de" #settings.EMAIL_ADMIN
            # to_email = ['bushaltestelle.80@web.de']#settings.EMAIL_RESPONSIBLE
            message = "This item is running low: {}.\nMinimum amount: {}\nCurrent amount: {}".format(pharmacyObject.name,
                                                                                                     pharmacyObject.alarm_value,
                                                                                                     pharmacyObject.available_quantity())
            subject = "FLI-Pharmacy: {} is running low".format(new_submission.pharmacy.name)
            #send_mail(subject, message, from_email, to_email, html_message=message)
        return HttpResponseRedirect('/')

@login_required
def seesubmissions(request, primary_key):
    order = get_object_or_404(Order, pk=primary_key)
    pharmacy = Pharmacy.objects.get(order__pk=primary_key)
    submissionlist = Submission.objects.filter(order__pk=primary_key).order_by('-date')

    #product= get_object_or_404(Order, pk=primary_key)
    #submissionlist = Submission.objects.filter(product__pk=primary_key).order_by('-date')
    #available_containers = product.available_containers()
    #available_quantity = product.available_quantity()
    #available_quantity_last_container = product.available_quantity_last_container()
    return render(request, 'submissions.html', {'order': order, 'submissions':submissionlist, 'pharmacy': pharmacy,})


@login_required
def allsubmissions(request, primary_key):
    pharmacy = get_object_or_404(Pharmacy, pk=primary_key)
    orderlist = Order.objects.filter(pharmacy__pk=primary_key)
    submissionlist = Submission.objects.filter(order__pharmacy__pk=primary_key).order_by('-date')
    #submissionlist =[]
    #for order in orderlist:
    #    submissionsfromorder = Submission.objects.filter(order__pk=order.pk).order_by('-date')
    #    submissionlist.extend(submissionsfromorder)
    s = SubmissionFilter(request.GET, queryset=submissionlist)
    return render(request, 'allsubmissions.html', {'filter': s,'submissions':submissionlist, 'pharmacy': pharmacy,'showgroups': True, })

@login_required
def showorders(request, primary_key):
    orderlist = Order.objects.filter(pharmacy__pk=primary_key)
    pharmacy = Pharmacy.objects.get(pk=primary_key)
    return render(request, 'orders.html', {'pharmacy': pharmacy, 'orders':orderlist,})


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
