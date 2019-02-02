from django.contrib import admin
from .models import Company, DrugClass, Pharmacy, Person, Submission, StockProduct
from django import forms
# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', )

@admin.register(DrugClass)
class DrugClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', )

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', )

@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_display = ('pharmacy','state','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed','available_containers','available_quantity')
    search_fields = ('pharmacy','state','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed')
    #ordering = ('pharmacy','pharmacy__name', )

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('application_number','date','person','amount_containers','quantity','comment','procedure_control')
    search_fields = ('application_number','date','person__name','amount_containers','quantity','comment','procedure_control')
    ordering = ('application_number','date','person__name','amount_containers','quantity','comment','procedure_control')

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    #list_display = ('name','state','molecule','type','company','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed')
    #search_fields = ('name','state','molecule','type','company__name','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed')
    list_display = ('name','company','state','dose','type','animal_species','umwidmungsstufe','storage_instructions','comment','attachment')
    search_fields = ('name','company__name','state','dose','type','animal_species','umwidmungsstufe','storage_instructions','attachment','comment')
    ordering = ('name','state',)

class SubmissionForm(forms.ModelForm):
    """
    Form for submission editing in admin
    """
    class Meta:
        model = Submission
        fields = ('application_number','product','date','person','amount_containers','quantity','comment','procedure_control')

class PharmacyForm(forms.ModelForm):
    """
    Form for pharmacy editing in admin
    """
    class Meta:
        model = Pharmacy
        #fields = ('name','state','molecule','drug_class','type','company','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number',)
        fields = ('name','state','drug_class','type',)

class StockProductForm(forms.ModelForm):
    """
    Form for pharmacy product editing in admin
    """
    class Meta:
        model = StockProduct
        fields = ('pharmacy','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number')