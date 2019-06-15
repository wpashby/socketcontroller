#------------------------------------------------------------------------------------------#
#Written by Bill Pashby
#ECE 306 Project 10
#
#
#Client-Side controller to control IoT-equiped embedded system over a TCP socket
#
#------------------------------------------------------------------------------------------#

import socket
from inputs import get_gamepad
import time
import sys


#------------------------------------------------------------------------------------------#
'''VARIABLES'''
#Socket setup vars
remote_ip = '10.139.000.111'#IP address of your IoT module
port = 21                   #The port you opened on your IoT module

#Transmitted string setup
indichar = '.'              #Inicator character
code = '1234'               #4-digit security code
messages = ""               #The whole message - filled before transmittion


#Controller input vars
analogvalueL = 0            #Value from left joystick (Y-axis)
analogvalueR = 0            #Value from right joystick (Y-axis)
sendvalueL = 0              #Remapped value from left joystick
sendvalueR = 0              #Remapped value from right joystick
sendstringL = ""            #Full string for left motor, including sign
sendstringR = ""            #Full string for left motor, including sign

#Number ranges for input and output
maxtriggervalue = 32767     #maximum value from a joystick
mintriggervalue = -32767    #minimum value from a joystick
maxsendvalue = 255          #maximum value sent to server
minsendvalue = -255         #mimimum value sent to server
#------------------------------------------------------------------------------------------#


#------------------------------------------------------------------------------------------#
'''SOCKET SETUP'''
try:                                                        #Starts socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print ('Failed to create socket.')                      #Faliure in socket creation
    sys.exit();                                             #Exits program
    
print ('Socket Created')                                    #Socket creation was successful

print ('Ip address is ' + remote_ip)
s.connect((remote_ip, port))                                #Connects client to car server
print ('Socket connection successful')
#------------------------------------------------------------------------------------------#


#------------------------------------------------------------------------------------------#
'''FUNCTIONS'''
#*****getinfo() will only return once there is a change in state on the gamepad*****

def getinfo():                      #Gets values from the gamepad every change of state
    events = get_gamepad()          #Updates the events data set with the current state
    
    for event in events:            #Operates on the most recent event, will not skip events
        
        stick = event.code          #Gets the input type
        stickval = event.state      #Gets the input value
        
        if stick == 'ABS_Y':        #Y-axis joystick
            global analogvalueL     #Sets appropriate global value from joystick
            analogvalueL = stickval
            
        elif stick =='ABS_RY':      #X-axis joystick
            global analogvalueR     #Sets appropriate global value from joystick
            analogvalueR = stickval


def rangemap(value):                #Maps the joystick values to an interpretable range
    return int((value-mintriggervalue)*(maxsendvalue-minsendvalue)/
               (maxtriggervalue-mintriggervalue)+minsendvalue)
#------------------------------------------------------------------------------------------#


#------------------------------------------------------------------------------------------#
'''MAIN LOOP'''
while True:
    getinfo()                                           #Updates the joystick values

    if (int(time.clock()*10))%2==0:                     #Execute five times a second

        #remaps trigger values to a 3-digit positive value
        sendvalueL = rangemap(analogvalueL)
        sendvalueR = rangemap(analogvalueR)

        #Changes remapped values to strings, and adds a '+' for positive values
        if sendvalueL >= 0:
            sendstringL = '+' + str("%03d" % (sendvalueL,))
        else:
            sendstringL = str("%04d" % (sendvalueL,))
        if sendvalueR >= 0:
            sendstringR = '+' + str("%03d" % (sendvalueR,))
        else:
            sendstringR = str("%04d" % (sendvalueR,))

        #concatenates various values into a single string
        message = (str(indichar) +                      #Indicator character
                   str(code) +                          #4-digit security code
                   sendstringL +        #Left motor PWM value
                   sendstringR +        #Right motor PWM value
                   '*'                  #End of string
                   '\r\n'                               #Carriage return and line feed
                   )
        s.sendall(message.encode(encoding='ascii'))     #Sends message after ascii-encoding
        print(message)                                  #Also prints message for debuggin
        time.sleep(0.2)                                 #waits for 200 milliseconds
#------------------------------------------------------------------------------------------#
