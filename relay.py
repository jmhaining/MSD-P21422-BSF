#--------------------------------------------------------------------
# File name: relay.py
# Author(s): Jennika Haining (jmh1592@rit.edu), Josh Noble (jtn6092@rit.edu)
# Date: 20 October 2020
# Project: MSD P21422 Black Soldier Fly Composting Smart Shed
# Purpose: To control devices used in maintaining a stable environment
#          based on data collected
# Notes:
#       Humidifier Pin = GPIO 16
#       Vent/Fan Pin   = GPIO 20
#       Heater Pin     = GPIO 21
#       Light pin      = GPIO 25
#
# To-Do: Change the print statements in check_data() to reflect data
#        and device being operated. I.e. "data value" to "temperature" or "humidity"
#
#        Ideally co2 and vent could work in check_data() as well, but vent is ON when co2 is HIGH
#        which is opposite heater and humidifier, which are OFF when temp or hum are HIGH
#--------------------------------------------------------------------

import RPi.GPIO as GPIO

def check_data(max_data, min_data, mid_data, curr_data, pin, device, verb):
    #check_data() contains the logic to turn devices on or off according the current data being recieved
    
    #If data (temp/hum) is too low and device (heater/humidifier) is not already on
    if (curr_data < min_data) & (device is False):
        #turn on the device using pin
        #GPIO.setmode(pin, 1)
        if verb:
            print("Data value is too low. Turning on device.")
    #If data is too high
    elif (curr_data > max_data):
        #Send alert, data is over max value (too high temp/too much humidity)
        #if device is on
        if device:
            pass
            #turn off device
            #GPIO.setmode(pin, 0)
        if verb: 
            print("Data value is too high")
    #If data is at acceptable level and heater is on
    elif (curr_data == mid_data) & device:
        #turn off the device
        #GPIO.output(pin, 0)
        if verb:
            print("Acceptable data value reached. Turning device off.")  
    else:
        pass
    return


#def check_co2(max_co2, min_co2, mid_co2, curr_co2, vent, verb):
    #if too high
        #open vent
    #if acceptable or too low and vent is open
        #close vent
    #else
        #pass
    #return

#def breeding_light(verb)
    #check 1
        #turn on light
    #check 2
        #turn off light
    #check 3
        #pass
    #return

def relay(curr_temp, curr_hum, curr_co2, verb):
    #GPIO.setmode(GPIO.BCM) 
    
    #Max and min are the maximum and minimum values temperature/humidity/co2 should reach
    #Ideal is the ideal value temperature/humidity/co2 should be at
    #Pins are the GPIO pins the devices will be connected too
    #Heater/humidifier/vent are the booleans indicating current status of the devices
        #0 is low or off, 1 is high or on
    #Verb is the verbose flag, which determines if printing to the shell is done
    
    max_temp = 100
    ideal_temp = 70
    min_temp = 55
    heat_pin = 16
    #heater = GPIO.input(heat_pin)
    
    max_hum = 100
    ideal_hum = 70
    min_hum = 50
    hum_pin = 20
    #humidifier = GPIO.input(hum_pin)
    
    max_co2 = 5000
    ideal_co2 = 2500
    min_co2 = 2000
    vent_pin = 21
    #vent = GPIO.input(vent_pin)
    
    print("Testing... temp:", curr_temp)
    
    #psuedo code
    #Check Temp
        #check_data(max_temp, min_temp, ideal_temp, curr_temp, heat_pin, heater, verb)
    #Check Humidity
        #check_data(max_hum, min_hum, ideal_hum, curr_hum, hum_pin, humidifier, verb)
    #Check CO2
        #def co2_vent(max co2, min co2)
    #Check light
        #breeding_light(time?)

##def init():
##    GPIO.setmode(GPIO.BCM)
##    #first time initialization code
##    GPIO.setup(16, GPIO.OUT)
##    GPIO.setup(20, GPIO.OUT)
##    GPIO.setup(21, GPIO.OUT)
##    GPIO.setup(25, GPIO.OUT)
##    return
##    
##if __name__ == '__main__':
##    main()
##else:
##    init()