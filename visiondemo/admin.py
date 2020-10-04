from django.contrib import admin

from .models import Person

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['first_name']
    pass

admin.site.register(Person, PersonAdmin)