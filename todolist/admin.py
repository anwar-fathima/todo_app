from django.contrib import admin
from .models import ToDo
# Register your models here.
class ToDoAdmin(admin.ModelAdmin):
    list_display = ['id','user','title','is_completed','created_at'] 

admin.site.register(ToDo,ToDoAdmin)