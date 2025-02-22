from django.contrib import admin
from .models import Note
# Register your models here.

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','description','is_enable','is_deleted']
    list_filter = ['is_enable']
    search_fields = ['title']
    ordering = ['is_enable']

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj = ...):
        return False
    
    def has_delete_permission(self, request, obj = ...):
        return False
    