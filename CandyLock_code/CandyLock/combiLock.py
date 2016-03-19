'''
CandyLock - main programme

Your candy machine is locked with a 4 token password. Place 1 token
at a time, if you get all of them right, the machine will give you 
a candy as reward.

It is driven by opencv. The programme take pictures of the token and 
match them to a pre-defined set(done by combiLock_train.py). 
'''
import imageRecognizer as recon
from Servo import *
import mraa
import time

led_pin_green=4
led_pin_red=5
led_pin_light=7
btn_pin=6

myServo = Servo("The lock")
myServo.attach(3)

iCorrect=True

def unlock():
    myServo.write(90)
    time.sleep(2)
    myServo.write(0)
    

if __name__=="__main__":
    led_green=mraa.Gpio(led_pin_green)
    led_green.dir(mraa.DIR_OUT)
    led_green.write(0)
    
    led_red=mraa.Gpio(led_pin_red)
    led_red.dir(mraa.DIR_OUT)
    led_red.write(0)
    
    led_light=mraa.Gpio(led_pin_light)
    led_light.dir(mraa.DIR_OUT)
    led_light.write(0)
    
    btn=mraa.Gpio(btn_pin)
    btn.dir(mraa.DIR_IN)
    btn.mode(mraa.MODE_PULLUP)
    
    myServo.write(0)
    
    recon.init()
    
    while True:
        for i in range(4):
            #wait for a token to activate the triggers
            while btn.read()==1:
                pass
                
            #blink the green led x times, don't move the token
            #after you placed it inside the machine
            for j in range(4):
                led_green.write(0)
                time.sleep(0.5)
                led_green.write(1)
                time.sleep(0.2)
            led_green.write(0)
            
            #Turn on the light, to light up the camera
            led_light.write(1)
            
            #Recognize the object
            res=recon.recognize()
            
            led_light.write(0)
            
            #If a wrong token is placed, or a mistake has
            #already happened, mark the sequence as wrong
            if iCorrect and res!=i:
                iCorrect=False
            
            #Make sure the trigger has been released
            while btn.read()==0:
                pass
            time.sleep(0.5)
        
        #The combination is correct, give candy
        if iCorrect==True:
            #Blink green led to show it's right
            for j in range(4):
                led_green.write(1)
                time.sleep(0.1)
                led_green.write(0)
                time.sleep(0.1)
            #Give a candy
            unlock()
        #The combination is incorrect
        else:
            #Red led indicates a fault
            led_red.write(1)
            time.sleep(2)
            led_red.write(0)
            