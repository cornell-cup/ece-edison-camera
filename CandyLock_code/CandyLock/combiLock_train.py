'''
CandyLock - training programme

Used before combiLock.py. Place a token in the machine, and wait for 
the programme to remember it. Repeat 4 times to make the combination.

After that, run combiLock.py to try your combination!

'''
import imageRecognizer as recon
import mraa
import time

led_pin_green=4
led_pin_red=5
led_pin_light=7
btn_pin=6

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
    
    recon.init()
    
    #Recognize 4 items as the combination
    for i in range(4):
        #wait for a token to activate the trigger
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
        
        #Train a token - remember one slot in the sequence
        recon.train(i)
        
        #Turn off the light
        led_light.write(0)
        
        #Make sure the trigger has been released
        while btn.read()==0:
            pass
        time.sleep(0.5)

