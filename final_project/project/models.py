from __future__ import unicode_literals
from datetime import datetime

from django.db import models, connection
from django.utils import timezone

class Data(models.Model):
	category = models.CharField(max_length = 200)
	value = models.IntegerField(default = 0)
	source = models.CharField(max_length = 200)
	time = models.DateTimeField(default=timezone.now)

	def deleteData(self):
		with connection.cursor() as cur:
			cur.execute('DELETE FROM project_data WHERE id = %s;', [self.id])