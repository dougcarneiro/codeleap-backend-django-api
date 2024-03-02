from django.contrib import admin

from ..core.models import BaseModelManager
from . import models

@admin.register(models.Career)
class CareerAdmin(admin.ModelAdmin):
    search_fields = [
        'username',
        'title',
    ]
    list_filter = ('is_private', 'is_active')
    list_display = ('username', 'title', 'is_private', 'is_active', 'created_at', 'updated_at')


    def get_queryset(self, request):
        return models.Career.all_objects

    raw_id_fields = ()