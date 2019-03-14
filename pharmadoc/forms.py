from django import forms
from .models import Pharmacy
from django.core.files.uploadedfile import SimpleUploadedFile

def pharmacy_choices():
    pharmacy = Pharmacy.objects.all()
    i=1
    choices_list = [[i,'---']]
    for p in pharmacy:
        i+=1
        choices_list.append([i,p.name + ' ' + p.dose])
    return choices_list

class addOrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(addOrderForm, self).__init__(*args, **kwargs)
        self.fields['pharmacy'] = forms.TypedChoiceField(choices=pharmacy_choices())
        self.fields['state'] = forms.TypedChoiceField(choices=((1, 'active'), (2, 'deactivated')))
        self.fields['amount'] = forms.IntegerField(label='Amount ordered Containers', min_value=1)
        self.fields['quantity'] = forms.DecimalField(label='Quantity one Container', min_value=1)
        self.fields['unit'] = forms.TypedChoiceField(choices=((1, '---'), (2, 'g'), (3, 'mg'), (4, 'ug'), (5, 'l'), (6, 'ml'), (7, 'ul')))
        self.fields['delivery'] = forms.DateField(label='Delivery date', widget=forms.SelectDateWidget)
        self.fields['expiry'] = forms.DateField(label='Expiry date', widget=forms.SelectDateWidget)
        self.fields['batch'] = forms.CharField(label='Batch number', max_length=100)
        self.fields['attachment'] = forms.FileField(required=False)
        self.fields['comment'] = forms.CharField(widget=forms.Textarea, required=False)
        self.fields['identifier'] = forms.CharField(max_length=100, required=False)

    """
    pharmacy = forms.ChoiceField(choices=pharmacy_choices()) #only refreshes values when the server is reset!!!
    state = forms.TypedChoiceField(choices=((1, 'active'), (2, 'deactivated')))
    amount = forms.IntegerField(label='Amount ordered Containers', min_value=1)
    quantity = forms.DecimalField(label='Quantity one Container', min_value=1)
    unit = forms.TypedChoiceField(choices=((1, '---'), (2, 'g'), (3, 'mg'), (4, 'ug'), (5, 'l'), (6, 'ml'), (7, 'ul')))
    delivery = forms.DateField(label='Delivery date', widget=forms.SelectDateWidget)
    expiry = forms.DateField(label='Expiry date', widget=forms.SelectDateWidget)
    batch = forms.CharField(label='Batch number', max_length=100)
    attachment = forms.FileField(required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False)
    identifier = forms.CharField(max_length=100, required=False)
    """


#file_data = {'pharmacyfile': SimpleUploadedFile('manual.pdf', <file data>)}





