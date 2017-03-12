from __future__ import unicode_literals

from django.db import models, connection

class Data(models.Model):
	category = models.CharField(max_length = 200)
	value = models.IntegerField(default = 0)
	source = models.CharField(max_length = 200)

	def addData(self):
		with connection.cursor() as cur:
			cur.execute("INSERT INTO DATA (category, value, source) VALUES (%s, %s, %s);", self.category, self.value, self.source)

	def deleteData(self):
		with connection.cursor() as cur:
			cur.execute("DELETE FROM DATA WHERE source = %s, value = %s;", self.source, self.value)

	def searchData(key):
		with connection.cursor() as cur:
			cur.execute("SELECT * FROM DATA WHERE id = %s", key)
	

