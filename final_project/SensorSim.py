import requests, sys, random, threading, time, math
from datetime import datetime

start = datetime.utcfromtimestamp(0)
def time(time):
	return (time - start).total_seconds() * 1000.0

def sendData(count):
    print("Send data called with arg=" + str(count))
    counter = 0
    #next_call = time.time()
    while counter != count:
		timeNow = time(datetime.now())
		print(timeNow)
		#r = requests.post("http://sqlinjections.herokuapp.com/api/data/", data={
		r = requests.post("http://localhost:8000/api/data/", data={
			"category" : "SensorSim",
			"source_id" : "df9312a5-f32c-4132-bef7-72a877c397e4",
			"value" : int(3 * math.sin(counter / 4.0)),
			"create_time": counter #int(time(datetime.now()))
			}, auth=("admin","password123"))
		print("[request number " + str(counter) + "]: status= " + str(r.status_code))

		counter = counter + 1

        #next_call = next_call+1;
        #time.sleep(next_call - time.time())

if __name__ == "__main__":
    count = -1
    if len(sys.argv) >= 1:
        count = int(sys.argv[1])

    #if count > 0:
    #    print("Sending up to " + str(count) + " data points.")
    #else:
    #    print("Sending continuously until terminated.")

	sendData(count)

    #timerThread = threading.Thread(target=sendData, args=(count))
    #timerThread.daemon = True
    #timerThread.start()
