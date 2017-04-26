import requests, sys, random, threading, time
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
		r = requests.post("http://localhost:8000/api/data/", data={
			"category" : "SensorSim",
			"source_id" : "e143fca3-bfd2-4416-b9cd-04663c362218",
			"value" : counter * counter,
			"create_time": int(time(datetime.now()))
			}, auth=("admin","password123"))
		print("[request number " + str(counter) + "]: status= " + str(r.status_code))

		counter = counter + 1

        #next_call = next_call+1;
        #time.sleep(next_call - time.time())

def test(x):
	return x

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
