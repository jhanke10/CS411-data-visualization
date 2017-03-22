from __future__ import unicode_literals
from datetime import datetime

import uuid

from django.db import models, connection
from django.utils import timezone

class NumericalData(models.Model):
	#For now, we push everything to just one sensor type. Later add multiple.
	#sensorID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	dataID   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name     = models.CharField(max_length = 200)
	time     = models.DateTimeField(default=timezone.now)
	value    = models.IntegerField(default = 0)

	#Useful for printing out data entries
	def __str__(self):
		return "NumericalData(dataID=" + str(self.dataID) + ", name=" + str(self.name) + ", time=" + str(self.time) + ", value=" + str(self.value) + ")"

	def addData(self, data):
		with connection.cursor() as cur:
			cur.execute('INSERT INTO project_data (category, value, source, time) VALUES (%s, %s, %s, %s);', [data.category, data.value, data.source, datetime.now()])

	def deleteData(self):
		with connection.cursor() as cur:
			cur.execute('DELETE FROM data_data WHERE ID = %s;', [self.ID])

	def searchData(self, data = None):
		if data == None:
			datapoint = self.objects.raw('SELECT * FROM project_data')
		else:
			datapoint = self.objects.raw('SELECT * FROM project_data WHERE ID = %s', [data.ID])
		return datapoint

	def updateData(self, data):
		with connection.cursor() as cur:
			cur.execute('UPDATE project_data SET category = %s, value = %s, source = %s WHERE time = %s', [data.category, data.value, data.source, data.time])
