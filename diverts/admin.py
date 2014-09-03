from django.contrib import admin

from diverts.models import Airfield, Navaid


class AirfieldAdmin(admin.ModelAdmin):
    list_display = ('ident', 'lat', 'lon')
    search_fields = ['ident']

class NavaidAdmin(admin.ModelAdmin):
    list_display = ('ident', 'name', 'components', 'lat', 'lon')
    search_fields = ['ident', 'name']

admin.site.register(Airfield, AirfieldAdmin)
admin.site.register(Navaid, NavaidAdmin)
