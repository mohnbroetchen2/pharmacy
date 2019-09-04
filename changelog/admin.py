from django.contrib import admin
from .models import Change

@admin.register(Change)
class ChangeAdmin(admin.ModelAdmin):
    """
    ChangeAdmin for Change model
    """
    list_display = ('version', 'change_type','short_text', 'description',)
    search_fields = ('version','change_type','short_text', 'description',)
    ordering = ('version','change_type')