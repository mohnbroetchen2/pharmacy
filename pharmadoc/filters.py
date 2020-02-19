"""
Filters: using django-filters to filter querysets
"""
import django_filters
from django_filters import FilterSet
from django.forms.widgets import CheckboxSelectMultiple
import django.forms
from .models import Order, Pharmacy, Person, Submission, DrugClass, Company

class OrderViewFilter(FilterSet):
    delivery_date = django_filters.DateFromToRangeFilter(label='Delivery date: (YYYY-MM-DD)')
    pharmacy = django_filters.ModelMultipleChoiceFilter(queryset=Pharmacy.objects.all(),widget=CheckboxSelectMultiple(),label="Pharmacy",label_suffix="",)
    class Meta:
        model = Order
        fields = ['delivery_date','batch_number','pharmacy']

class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = ['pharmacy','batch_number']

class PharmacyFilter(FilterSet):
    class Meta:
        model = Pharmacy
        fields = ['name','company',]

class SubmissionFilter(FilterSet):
    application_number = django_filters.CharFilter(lookup_expr='icontains',  label='Application #')
    class Meta:
        model = Submission
        fields = ['application_number','order','person','date',]
