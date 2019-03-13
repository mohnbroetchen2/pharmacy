from django_filters import FilterSet
from .models import Change

class ChangeFilter(FilterSet):
    class Meta:
        model = Change
        fields = ['id','change_type','version',]
