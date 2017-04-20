from __future__ import unicode_literals
from datetime import datetime
import uuid

from django.db import models, connection

start = datetime.utcfromtimestamp(0)

def time(time):
	return (time - start).total_seconds() * 1000.0

class User(models.Model):
	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	username = models.CharField(max_length = 200)
	password = models.CharField(max_length = 200)

	def deleteUser(self):
		with connection.cursor() as cur:	
			cur.execute('DELETE FROM project_user WHERE user_id = %s;', [self.user_id])

class Source(models.Model):
	source_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	source_name = models.CharField(max_length = 200, default = '')
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def deleteSource(self):
		with connection.cursor() as cur:	
			cur.execute('DELETE FROM project_source WHERE source_id = %s;', [self.source_id])

class Data(models.Model):
	data_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	source = models.ForeignKey(Source, on_delete=models.CASCADE)
	category = models.CharField(max_length = 200)
	value = models.IntegerField(default = 0)
	time = models.IntegerField(default=time(datetime.now()), editable = False)

	def deleteData(self):
		with connection.cursor() as cur:	
			cur.execute('DELETE FROM project_data WHERE data_id = %s;', [self.data_id])