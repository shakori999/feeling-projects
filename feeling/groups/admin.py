from django.contrib import admin
from .models import *

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


admin.site.register(Family)
admin.site.register(Company)
