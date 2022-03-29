#refer to http://blog.sipeed.com/p/677.html
import sensor,image,lcd,time, network
import KPU as kpu
import ubinascii
from machine import unique_id
from time import sleep
import _thread
import lcd
import time

from Maix import GPIO
from fpioa_manager import fm


if __name__ == "__main__":
    # It is recommended to callas a class library (upload network_espat.py)
    sleep(20)
    # from network_esp32 import wifi
    SSID = "PiNetwork"
    PASW = "herber2001"

    def check_wifi_net(retry=5):
        if wifi.isconnected() != True:
            for i in range(retry):
                try:
                    wifi.reset(is_hard=True)
                    print('Connecting Sipeed Maix to wifi...')
                    wifi.connect(SSID, PASW)
                    if wifi.isconnected():
                        break
                except Exception as e:
                    print(e)
            return wifi.isconnected()

        if wifi.isconnected() == False:
            check_wifi_net()

    print(check_wifi_net())
    import uos

    print(uos.listdir("/sd/"))




    lcd.init(freq=15000000)
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_vflip(1)
    sensor.run(1)
    clock = time.clock()
    classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']
    print(uos.listdir("/sd/"))
    task = kpu.load("/sd/20class.kmodel")
    anchor = (1.08, 1.19, 3.42, 4.41, 6.63, 11.38, 9.42, 5.11, 16.62, 10.52)
    a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
    #lcd.rotation(1)
    #lcd.mirror(True)
    client_id = ubinascii.hexlify(unique_id())

    client = MQTTClient(client_id, "192.168.255.1")
    client.connect()

    while(True):
        clock.tick()
        img = sensor.snapshot()
        code = kpu.run_yolo2(task, img)
        print(clock.fps())
        if code:
            print(code)
            for i in code:
                a=img.draw_rectangle(i.rect())
                img.draw_string(i.x(), i.y(), classes[i.classid()], color=(255, 0, 0), scale=2)
                img.draw_string(i.x(), i.y()+24, '%.3f'%i.value(), color=(255, 0, 0), scale=2)
                a = lcd.display(img)
                client.publish("warnings/sipeed", classes[i.classid()])
        else:
            a = lcd.display(img)
    a = kpu.deinit(task)

