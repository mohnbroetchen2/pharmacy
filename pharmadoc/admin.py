from django.contrib import admin
from .models import Company, DrugClass, Pharmacy, Person, Submission, Order, Molecule, Vendor, Mixed_Submission,License_Number
from .models import Mixed_Pharmacy, Mixed_Solution, Submission_For_Mixed_Solution
from django import forms
import csv
from django.http import HttpResponse
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
# Register your models here.

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "Export Selected"

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', )
    actions = ["export_as_csv"]

@admin.register(DrugClass)
class DrugClassAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', )
    actions = ["export_as_csv"]

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', )
    actions = ["export_as_csv"]

@admin.register(Molecule)
class MoleculeAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', )
    actions = ["export_as_csv"]

@admin.register(License_Number)
class License_NumberAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('license','state')
    search_fields = ('license',)
    ordering = ('license','state')
    actions = ["export_as_csv"]

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', )
    actions = ["export_as_csv"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('pk','pharmacy','identifier','vendor','state','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','available_containers','available_quantity')
    search_fields = ('pharmacy__name','identifier','vendor__name','state','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number',)
    #ordering = ('pharmacy','pharmacy__name', )
    readonly_fields = ('identifier',)
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Only set identifier during the first save.
            stringdate = str(obj.delivery_date)
            new_identifier =  obj.pharmacy.name[:3] + stringdate[2:] 
            existingOrder = Order.objects.filter(identifier=new_identifier)
            if existingOrder:
                found = 1
                i=2
                while found == 1: 
                    temp_identifier =new_identifier+"_"+str(i)
                    existingOrder = Order.objects.filter(identifier=temp_identifier)
                    if existingOrder:
                        i=i+1
                    else:
                        found = 0
                obj.identifier = new_identifier+"_"+str(i)
            else:
                obj.identifier = new_identifier

        super().save_model(request, obj, form, change)
    list_filter = (('pharmacy', RelatedDropdownFilter),
                   ('identifier', DropdownFilter),
                   ('vendor__name', DropdownFilter),
                   'state',
                   ('amount_containers', DropdownFilter),
                   ('quantity', DropdownFilter),
                   ('unit', DropdownFilter),
                   ('delivery_date', DropdownFilter),
                   ('expiry_date', DropdownFilter),
                   ('batch_number', DropdownFilter))
    actions = ["export_as_csv"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('application_number','order','date','person','license','amount_containers','quantity','comment','procedure_control')
    search_fields = ('date','application_number','person__name','license__license','amount_containers','quantity','comment','procedure_control')
    ordering = ('-date','order__pharmacy','application_number','person__name','amount_containers','quantity','comment','procedure_control')
    list_filter = ('order',
                    ('application_number', DropdownFilter),
                   ('date', DropdownFilter),
                   'person',
                   ('license__license',DropdownFilter),
                   ('amount_containers', DropdownFilter),
                   ('quantity', DropdownFilter),
                   ('comment', DropdownFilter),
                   ('procedure_control', DropdownFilter))
    actions = ["export_as_csv"]

@admin.register(Mixed_Submission)
class Mixed_SubmissionAdmin(admin.ModelAdmin):
    list_display = ('name','application_number','date','person','comment',)
    search_fields = ('name','date','application_number','person__name','comment',)
    ordering = ('-date','name','application_number','person__name','comment','procedure_control')
    list_filter = (('application_number', DropdownFilter),
                   ('date', DropdownFilter),
                   'person',
                   ('comment', DropdownFilter),)
    actions = ["export_as_csv"]

@admin.register(Mixed_Pharmacy)
class Mixed_SubmissionAdmin(admin.ModelAdmin):
    list_display = ('name','state')
    search_fields = ('name','state')
    ordering = ('name','state')

@admin.register(Mixed_Solution)
class Mixed_SolutionAdmin(admin.ModelAdmin):
    list_display = ('identifier','state','amount_containers','quantity','unit','mixed_date','expiry_date')
    search_fields = ('identifier','state')
    ordering = ('identifier','state','amount_containers','quantity','unit','mixed_date','expiry_date')
    class Meta:
        model = Mixed_Solution
        fields = ('identifier','state','amount_containers','quantity','unit','mixed_date','expiry_date')

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin, ExportCsvMixin):
    #list_display = ('name','state','molecule','type','company','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed')
    #search_fields = ('name','state','molecule','type','company__name','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed')
    list_display = ('name','company','state','type','animal_species','umwidmungsstufe','storage_instructions','comment','attachment')
    search_fields = ( 'name','company__name','state','drug_class__name','type','molecule__name','animal_species','umwidmungsstufe','storage_instructions','attachment','comment')
    ordering = ('name','state',)
    list_filter = (
                    ('company',RelatedDropdownFilter),
                   ('state',DropdownFilter),
                   ('type',DropdownFilter),
                   ('animal_species',DropdownFilter),
                   ('umwidmungsstufe',DropdownFilter),
                   ('storage_instructions',DropdownFilter),
                   ('comment',DropdownFilter))
    actions = ["export_as_csv"]
   
class SubmissionForm(forms.ModelForm):
    """
    Form for submission editing in admin
    """
    class Meta:
        model = Submission
        fields = ('application_number','order','date','person','amount_containers','quantity','comment','procedure_control')

class PharmacyForm(forms.ModelForm):
    """
    Form for pharmacy editing in admin
    """
    class Meta:
        model = Pharmacy
        #fields = ('name','state','molecule','type','company','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number',)
        fields = ('name','state','type','identifier_shortcut',)

class OrderForm(forms.ModelForm):
    """
    Form for pharmacy order editing in admin
    """
    class Meta:
        model = Order
        fields = ('pharmacy','vendor','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number')

