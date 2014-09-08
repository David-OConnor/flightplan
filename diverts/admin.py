from django.contrib import admin

from diverts.models import Airfield, Runway, Navaid, Fix


class AirfieldAdmin(admin.ModelAdmin):
    list_display = ('ident', 'name', 'lat', 'lon')
    search_fields = ['ident']


class RunwayAdmin(admin.ModelAdmin):
    list_display = ('airfield', 'number', 'length', 'width')
    search_fields = ['airfield__ident']


class NavaidAdmin(admin.ModelAdmin):
    list_display = ('ident', 'name', 'components', 'lat', 'lon')
    search_fields = ['ident', 'name']


class FixAdmin(admin.ModelAdmin):
    list_display = ('ident', 'lat', 'lon')
    search_fields = ['ident']

admin.site.register(Airfield, AirfieldAdmin)
admin.site.register(Runway, RunwayAdmin)
admin.site.register(Navaid, NavaidAdmin)
admin.site.register(Fix, FixAdmin)
