# socketcontroller
## Description:
* Programmed by Bill Pashby
* Written using a Python 3.6.3 interpreter - might not work with Python 2.7
* Script to send signals to the IoT module over a TCP socket
* Set up for a gamepad as input, could be configured using other inputs

## Operation:
* Connect a gamepad to a computer
* With the car turned on, run the script
* After connecting to the car, the script will output any change of state of the joysticks every 0.2 seconds
* Command structure:
  * .1234+000+000
    * First character is the indicating character that tells the car to listen
    * The 1234 is the security code
    * The next 4 characters are the PWM values for the left motor, with the first being a sign (+/-) and the next 3 a 8-bit BCD value
    * The last 4 are for the right motor

## Setup:
* Install Python 3.6
  * https://www.python.org/downloads/release/python-360/
  * Files at bottom of page
* Install the inputs library
  * If using python 3, enter the following command in windows command prompt:
  * ```pip install inputs```

## Need to configure:
* remote_ip
  * Set to the IP address of your IoT module
* port
  * Set to the port that was set during socket setup on the IoT module
* indichar
  * Indicating character that is recognized by the server-side code
* code
  * 4-digit 'security' code used to prevent peer-to-peer interference

## Optional configurations:
* maxsendvalue and minsendvalue
  * These are the maximum and minimum values sent to the device for PWM

## Server-side configuration:
**Will not work for spring 2019 - Use command given in datasheet**
* Send the following command to the IoT device. Port number is interchangable, but must match client port.
  * ```AT+S.SOCKD=21```
  
## Additional notes:
* This is set up to send data every 0.2 seconds while there is an active change of state from the controller.
* Due to the nature of the input library being used, the "get input" function call will only return on a change of state. So, if there is no input from the device, the data will not send. A constant stream of data can be sent by either slightly moving the joysticks at all times, or use another finger to lightly toggle another button. Given that the joysticks output a 16-bit signed integer, overcoming this problem will not be hard
