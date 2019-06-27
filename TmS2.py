import serial
import time
import sys
from _thread import start_new_thread


addr = "0012" #please change your address according to the device number
msg = "Iseeyou" #just a message for our write method
bc = "RTI" #our broadcast-shortcut to get recognized by other devices

#known addresses
table = []

ser = serial.Serial(
    port = '/dev/ttyS0',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS
    )

#ser.isOpen()

#receiving outputs
def output():
    op = "".encode()
    while ser.inWaiting() > 0:
        op+=ser.read(1)
    time.sleep(1)
    return op.decode('UTF-8')

#broadcast your existence every 15 seconds
def broadcast():
    while True:
    	ser.write(str.encode("AT+DEST=FFFF\r\n"))
        time.sleep(1)
        ser.write(("AT+SEND={0}\r\n".format(len(bc)).encode("UTF-8")))
        time.sleep(1)
        ser.write(("{0}\r\n".format(bc)).encode("UTF-8"))
        print("Broadcast {0}".format(bc))
        time.sleep(60)

#send a message to every device in the table
def write():
    while True:
        print("Write")
        for i in table:
            print("Writing {0}".format(table[i]))
            ser.write(str.encode("AT+DEST={0}\r\n".format(table[i])))
            time.sleep(1)
            ser.write(str.encode("AT+SEND={0}\r\n".format(len(msg))))
            time.sleep(1)
            ser.write(str.encode("{0}\r\n".format(msg)))
            print("Write {0}".format(msg))
            time.sleep(1)
        time.sleep(30)

#just listening for other devices. if someone is broadcasting with a message "RTI" we'll save the device to our table
def listen():
    while True:
        answer = output()
        if answer != "":
            print("Listen: {0}".format(answer))
            if "RTI" in answer:
                muh = answer.split(",") #LR,XXXX,03,RTI 
                if muh[1] not in table:
                    table.append(muh[1])
                    print("New entry: ")
                    print(table)

#initialize your own address
def init():
    print("init: ")
    ser.write(("AT+ADDR={0}\r\n".format(addr)).encode("UTF-8"))
    time.sleep(1)
    answer1 = output()
    print("address changed " + answer1)
    ser.write(str.encode("AT+ADDR?\r\n"))
    time.sleep(2)
    answer2 = output()
    print("new address is " + answer2)

#here starts the active part of our program
init()
start_new_thread(listen, ())
start_new_thread(broadcast, ())


#while runtime it s possible to have access to several options
while 1:
	#looking for input
    eingabe = input()
    #show table with entries/devices we received RTI messages from
    if eingabe == "table":
        print(table)
    #if you write a device number it checks for the device in the table
    #in case of an entry you can send a message to that specific device
    elif eingabe in table:
        print("Your message...:")
        message = input()
        ser.write(str.encode("AT+DEST={0}\r\n".format(eingabe)))
        time.sleep(1)
        ser.write(str.encode("AT+SEND={0}\r\n".format(len(message))))
        time.sleep(1)
        ser.write(str.encode("{0}\r\n".format(message)))
    #to close/end the program
    elif eingabe == "exit":
        ser.close()
        sys.exit(0)
    #every other input delivers thi mesage
    else:
        print("{0} doesnt exist!".format(eingabe))








