from __future__ import unicode_literals

from django.db import models, connection

class Data(models.Model):
	category = models.CharField(max_length = 200)
	value = models.IntegerField(default = 0)
	source = models.CharField(max_length = 200)
