"""
Filters: using django-filters to filter querysets
"""
import django_filters
from django_filters import FilterSet
from .models import StockProduct, Pharmacy, Person, Submission, DrugClass, Company

class StockProductFilter(FilterSet):
    class Meta:
        model = StockProduct
        fields = ['pharmacy','batch_number','company']