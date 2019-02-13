"""
Filters: using django-filters to filter querysets
"""
import django_filters
from django_filters import FilterSet
from .models import Order, Pharmacy, Person, Submission, DrugClass, Company

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
