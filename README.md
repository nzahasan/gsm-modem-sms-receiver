SMS Reciever
===================
This python program receives sms from a gsm modem using at command and sends it to a server via post request.

----------

Dependency
-------------
These external python library was used in this program

> - pyserial (https://pypi.python.org/pypi/pyserial)
> - requests (https://pypi.python.org/pypi/requests/)
> - configparser (https://pypi.python.org/pypi/configparser)
> - termcolor (https://pypi.python.org/pypi/termcolor)

Usage
--------
To use this first you need to edit `config.ini`.  Place the right port , and baudrate. If you need to send message to a server in server section set `send: true` and put the address of the server.

>[Device]  
>Port: /dev/ttyUSB0  
>Baud_Rate: 115200  
  
>[Server]  
>Send: true  
>Address: http://localhost/receive.php  

If you dont know what is your port use `dmesg | grep tty` command to find the port address of your USB serial device. 
Then make the program executable using `sudo chmor +x receive.py`.
To execute the program use `sudo ./receive.py`
