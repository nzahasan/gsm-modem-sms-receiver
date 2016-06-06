#!/usr/bin/env python3
import serial, time, requests, re, configparser
from termcolor import cprint

# write command and read response
def writeNread(modem,WriteCMD):
	if WriteCMD != None:
		modem.write(bytearray(WriteCMD,"ascii"))
		time.sleep(0.1)
	
	response=b""
	waitByte = modem.inWaiting()
	while waitByte>0:
		response+=modem.read(waitByte)
		waitByte = modem.inWaiting()
	
	return response.decode("ascii")

# delete a sms
def DeleteMsg(modem, index):
	response=writeNread(modem,"AT+CMGD="+index+"\r")
	# check if deleted #
	if response.find("OK") != -1:
		cprint ("✅ Deleted from modem memory.","green")

def main():
	# read configFile #
	try:
		config = configparser.ConfigParser()
		config.read("config.ini")

		port = config.get("Device","Port")
		baudrate = int(config.get("Device","Baud_Rate"))
		send2server = config.get("Server","Send")
		URL = config.get("Server","Address")
	except:
		cprint("⚞ Config read error!","red")
		return

	# call modem
	try:
		modem = serial.Serial(port,baudrate,timeout=1)
		
		if modem.isOpen()!=True:
			cprint("⚞ Modem is not open!","red")
			return
	except:
		cprint("⚞ Modem connection error!","red")
		return

	cprint("Initializing Modem...","magenta") 

	# reset to factory default
	writeNread(modem,"AT&F0\r")
	# disable command echo
	writeNread(modem,"ATE0\r")
	# enable text mode
	writeNread(modem,"AT+CMGF=1\r")
	# notification at receive
	writeNread(modem,"AT+CNMI=1,1,0,1,0\r")

	cprint("Receiving SMS...","magenta")

	try:
		# checking notification @100ms interval
		while True:
			time.sleep(0.1)
			
			notification = writeNread(modem,None)

			#if noti received
			if len(notification)>0:
				notification = notification.replace("\r\n","")

				# notification format ->
				# \r\n+CMTI: "ME",23\r\n || \r\n+CMTI: "SM",23\r\n
				if notification.find("+CMTI:") != -1:

					index=notification.split(",")[1]

					msg = writeNread(modem,"AT+CMGR="+index+"\r")

					try:
						
						number = re.findall(r'(?<=",")([0-9+]+)(?=",,")',msg)[0]

						text = re.findall(r'(?<="\r\n)([\w\W]*)(?=[\r\n]{4}OK[\r\n]{2})',msg)[0] 
						
						cprint("[Sender]","cyan")	
						print(number)   
						
						cprint ("[Text]","cyan")
						print(text)
					except:
						cprint ("⚞ Messege read error!","red")

					# sending to server
					if send2server == "true":
						try:
							response =  requests.post(URL,{'sender': number,'text': text})
							if response.status_code == 200:
								cprint("✅ Sent to server.","green")
								DeleteMsg(modem, index)
							else:
								cprint("⚞ Server returned error: "+response.status_code,"red")
						except:
							cprint("⚞ Server unresponsive!","red")
	
	except KeyboardInterrupt:
		modem.close()
		cprint("\nGood Bye.","magenta")
		return

if __name__=="__main__":
	main()
