from Wifi import Wifi
import lcd

if __name__ == "__main__":
    # It is recommended to callas a class library (upload network_espat.py)

    # from network_esp32 import wifi
    SSID = "NETGEAR95"
    PASW = "dailyplanet779"

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
    print("ping google.com:", wifi.nic.ping("google.com"), "ms")


    lcd.init()
    lcd.draw_string(100, 100, ('network state:', wifi.isconnected(), wifi.ifconfig()), lcd.RED, lcd.BLACK)
