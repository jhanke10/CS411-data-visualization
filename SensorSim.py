import requests, sys, random, threading, time
import requests, sys, random, threading, time, math
from datetime import datetime

start = datetime.utcfromtimestamp(0)
@@ -12,10 +12,10 @@ def sendData(count):
    while counter != count:
		timeNow = time(datetime.now())
		print(timeNow)
		r = requests.post("http://localhost:8000/api/data/", data={
		r = requests.post("http://sqlinjections.herokuapp.com/api/data/", data={
			"category" : "SensorSim",
			"source_id" : "e143fca3-bfd2-4416-b9cd-04663c362218",
			"value" : counter * counter,
			"source_id" : "1221b9e4-0801-4771-bb50-fc82142aed65",
			"value" : int(12 * math.sin(counter / 12.0)),
			"create_time": int(time(datetime.now()))
			}, auth=("admin","password123"))
		print("[request number " + str(counter) + "]: status= " + str(r.status_code))
