from django.contrib import admin

from .models import Data, Source, User


class DataAdmin(admin.ModelAdmin):
	list_display = ['category', 'value', 'source', 'time']
	class Meta:
		model = Data

class SourceAdmin(admin.ModelAdmin):
	list_display = ['source_id', 'source_name', 'user']
	class Meta:
		model = Source

class UserAdmin(admin.ModelAdmin):
	list_display = ['user_id', 'username', 'password']
	class Meta:
		model = User

admin.site.register(Data, DataAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(User, UserAdmin)
