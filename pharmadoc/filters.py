"""
Filters: using django-filters to filter querysets
"""
import django_filters
from django_filters import FilterSet
from .models import Product, Pharmacy, Person, Submission, DrugClass, Company

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = ['pharmacy','batch_number']