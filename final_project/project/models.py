from __future__ import unicode_literals
from datetime import datetime

from django.db import models, connection
from django.utils import timezone

class Data(models.Model):
	category = models.CharField(max_length = 200)
	value = models.IntegerField(default = 0)
	source = models.CharField(max_length = 200)
	time = models.DateTimeField(default=timezone.now, primary_key = True)

	def addData(self, data):
		with connection.cursor() as cur:
			cur.execute('INSERT INTO project_data (category, value, source, time) VALUES (%s, %s, %s, %s);', [data.category, data.value, data.source, datetime.now()])

	def deleteData(self, data):
		with connection.cursor() as cur:
			cur.execute('DELETE FROM project_data WHERE time = %s;', [data.time])

	def searchData(self, data = None):
		if data == None:
			datapoint = self.objects.raw('SELECT * FROM project_data')
		else:
			datapoint = self.objects.raw('SELECT * FROM project_data WHERE time = %s', [data.time])
		return datapoint

	def updateData(self, data):
		with connection.cursor() as cur:
			cur.execute('UPDATE project_data SET category = %s, value = %s, source = %s WHERE time = %s', [data.category, data.value, data.source, data.time])
