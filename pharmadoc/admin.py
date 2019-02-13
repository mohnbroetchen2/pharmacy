from django.contrib import admin
from .models import Company, DrugClass, Pharmacy, Person, Submission, Order, Molecule
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

@admin.register(Molecule)
class MoleculeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pharmacy','identifier','state','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','available_containers','available_quantity')
    search_fields = ('pharmacy','identifier','state','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number',)
    #ordering = ('pharmacy','pharmacy__name', )
    readonly_fields = ('identifier',)
    def save_model(self, request, obj, form, change):
        if not obj.pk: # Only set identifier during the first save.
            stringdate = str(obj.delivery_date)
            new_identifier =  obj.pharmacy.name[:3] + stringdate[2:] 
            existingOrder = Order.objects.get(identifier=new_identifier)
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


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('application_number','date','person','amount_containers','quantity','comment','procedure_control')
    search_fields = ('application_number','date','person__name','amount_containers','quantity','comment','procedure_control')
    ordering = ('application_number','date','person__name','amount_containers','quantity','comment','procedure_control')

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    #list_display = ('name','state','molecule','type','company','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed')
    #search_fields = ('name','state','molecule','type','company__name','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number','consumed')
    list_display = ('name','company','state','type','animal_species','umwidmungsstufe','storage_instructions','comment','attachment')
    search_fields = ( 'name','company__name','state','type','animal_species','umwidmungsstufe','storage_instructions','attachment','comment')
    ordering = ('name','state',)
   
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
        fields = ('name','state','type',)

class OrderForm(forms.ModelForm):
    """
    Form for pharmacy order editing in admin
    """
    class Meta:
        model = Order
        fields = ('pharmacy','amount_containers','quantity','unit','delivery_date','expiry_date','batch_number')