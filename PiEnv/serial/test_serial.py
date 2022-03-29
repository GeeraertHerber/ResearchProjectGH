import serial
from time import sleep
test_string = "Test serial port ...".encode('utf-8')
port_list = ["/dev/serial0","/dev/ttyAMA0","/dev/ttyAMA0","/dev/ttyS0","/dev/ttyS"]
sleep(1)
for port in port_list:
  try:
    serialPort = serial.Serial(port, 9600, timeout = 2)
    print ("Serial port", port, " ready for test :")
    bytes_sent = serialPort.write(test_string)
    print ("Sended", bytes_sent, "byte")
    loopback = serialPort.read(bytes_sent)
    if loopback == test_string:
      print ("Received ",len(loopback), "bytes. Port", port,"is OK ! \n")
    else:
      print ("Received incorrect data:", loopback, "on serial part", port, "loopback \n")
    serialPort.close()
  except IOError as e:
    print ("Error on", port,"\n")
    print(e)
