from django.contrib import admin

from .models import Person, Phones

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    pass

class PhonesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin)
admin.site.register(Phones, PhonesAdmin)