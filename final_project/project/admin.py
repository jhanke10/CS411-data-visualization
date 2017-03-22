from django.contrib import admin

from .models import NumericalData


class NumericalDataAdmin(admin.ModelAdmin):
	list_display = ['dataID', 'name', 'time', 'value']
	class Meta:
		model = NumericalData

admin.site.register(NumericalData, NumericalDataAdmin)
