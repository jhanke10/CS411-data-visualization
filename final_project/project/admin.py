from django.contrib import admin

from .models import Data


class DataAdmin(admin.ModelAdmin):
	list_display = ['category', 'value', 'source', 'time']
	class Meta:
		model = Data

admin.site.register(Data, DataAdmin)
