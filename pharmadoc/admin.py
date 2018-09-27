from django.contrib import admin
from .models import Company, DrugClass, Pharmacy, Person, Submission
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

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('application_number','pharmacy','date','person','amount_containers','quantity','comment','procedure_control')
    search_fields = ('application_number','pharmacy','date','person__name','amount_containers','quantity','comment','procedure_control')
    ordering = ('application_number','pharmacy','date','person__name','amount_containers','quantity','comment','procedure_control')

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name','state','molecule','type','company','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed')
    search_fields = ('name','state','molecule','type','company__name','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed')
    ordering = ('name','state',)

class SubmissionForm(forms.ModelForm):
    """
    Form for submission editing in admin
    """
    class Meta:
        model = Submission
        fields = ('application_number','pharmacy','date','person','amount_containers','quantity','comment','procedure_control')

class PharmacyForm(forms.ModelForm):
    """
    Form for pharmacy editing in admin
    """
    class Meta:
        model = Pharmacy
        fields = ('name','state','molecule','drug_class','type','company','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number',)