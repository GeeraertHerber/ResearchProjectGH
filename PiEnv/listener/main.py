from pydoc import cli
from paho.mqtt.client import Client
from time import sleep
from models.Lidar import Lidar
import json
from threading import Thread
import serial
led_status = {"yellow_right":0, "yellow_left": 0, "red_right": 0, "red_left": 0, "blue":0}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    global scanner_list
    if msg.topic == "warnings/sipeed":
        # print(str(msg.payload))
        scanner_list.insert(0,msg.payload)
        # print(scanner_list)
        check_list(msg.payload, scanner_list, client)
    if msg.topic == "warnings/pi":
        lidar_data(msg.payload)

def lidar_data(payload):
    try: 
        data = dict(json.loads(payload))
        if data["range"] < 200:
            send_sequence(["red_right","yellow_right", "yellow_left", "red_left"], 0.3, 4)
        elif data["range"] < 500:
            send_sequence(["yellow_right", "yellow_left"], 0.4, 5) 
        elif data["range"] < 1200:
            send_signal('yellow_left', 1)
            send_signal('yellow_right', 1)
        elif data["range"] >1200:
            pass
    except: 
        pass

def send_signal(led, signal):
    global client, led_status
    payload = json.dumps({"led":led, 
    "signal":signal })
    client.publish("warnings/esp/leds", payload)
    led_status[led] = signal
    if signal == 1 and led != "blue": 
        Thread(target=check_led, args=(led, client,)).start()

def send_sequence(sequence, timing, repeat):
    global client
    payload = json.dumps({"sequence":sequence, 
            "timing":timing, 
            "repeat": repeat})
    client.publish("warnings/esp/leds", payload)

def check_list(payload, scanner_list, client):
    global led_status
    counter = scanner_list.count(payload)
    payload = payload.decode('utf-8')
    if (str(payload) == "car"):
        if counter > 2:
            # print("Sending payload")
            send_sequence(["red_right", "red_left"], 0.2, 3)
        if (counter > 1):
            # print("Sending payload")
            send_sequence(["yellow_right", "yellow_left"], 0.2, 3)
    elif (str(payload) == "person"):
        led = "yellow_right"
        if (counter > 2):
            print("Sending payload")
            signal = 1
            send_signal(led, signal)
        else:
            send_signal(led, 0)
    elif (str(payload) == "bicycle"):
        if (counter > 1):
            print("Sending payload")
            payload = json.dumps({"sequence":["yellow_right"], 
            "timing":0.4, 
            "repeat": 2})
            client.publish("warnings/esp/leds", payload)
    

def check_led(led, client):
    global led_status
    sleep(5)
    if led_status[led] == 1:
        payload = json.dumps({"led":led, 
            "signal":0 })
        client.publish("warnings/esp/leds", payload)

def clean_list(scanner_list):
    while len(scanner_list) > 20:
        del scanner_list[-1]
    return scanner_list

def ground_sensor():
    global THREAD_STATUS
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    signal = 0
    signal_before = 0
    while THREAD_STATUS:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            if float(line) < 3:
                signal = 1
                if signal != signal_before:
                    send_signal("blue", signal)
                    signal_before = signal
            else: 
                signal = 0
                if signal != signal_before:
                    send_signal("blue", 0)
                    signal_before = signal

def read_lidar():
    global THREAD_STATUS, client
    lidar = Lidar()
    lidar.connect_lidar()
    counter = 0
    while THREAD_STATUS: 
        data = lidar.read_lidar()
        if counter == 100: 
            client.publish("warnings/pi", json.dumps(data))
            counter = 0
        counter += 1

if __name__ == "__main__":
    try: 
        scanner_list = []
        client = Client()
        client.on_connect = on_connect
        client.on_message = on_message


        client.connect("192.168.255.1", 1883, 60)
        client.subscribe("warnings/sipeed")
        client.subscribe("warnings/pi")
        client.loop_start()  
        scanner_list = []
        THREAD_STATUS = True
        Thread(target=ground_sensor).start()
        Thread(target=read_lidar).start()

        while True: 
            sleep(0.1)
            scanner_list.insert(0,0)  
            scanner_list = clean_list(scanner_list)

    except: 
        THREAD_STATUS = False
        client.loop_stop()
        exit()