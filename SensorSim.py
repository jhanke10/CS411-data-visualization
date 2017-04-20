import requests, sys, random, datetime, threading, time

def sendData(count):
    print("Send data called with arg=" + str(count))
    counter = 0
    next_call = time.time()
    while counter != count:
        r = requests.post("http://localhost:8000/api/", data={
                "category" : "SensorSim",
                "source" : "sensor",
                "value" : random.randrange(0, 120)
            }, auth=("admin","password123"))
        print("[request number " + str(counter) + "]: status= " + str(r.status_code))

        counter = counter + 1

        next_call = next_call+1;
        time.sleep(next_call - time.time())

if __name__ == "__main__":
    count = -1
    if len(sys.argv) >= 1:
        count = int(sys.argv[1])

    if count > 0:
        print("Sending up to " + str(count) + " data points.")
    else:
        print("Sending continuously until terminated.")

    timerThread = threading.Thread(target=sendData, args=(count))
    timerThread.daemon = True
    timerThread.start()
