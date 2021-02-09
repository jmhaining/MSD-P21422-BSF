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

def check_data(d_max, d_min, d_curr, pin, verb):
    #A range is necessary to prevent the relay from flipping continually as the
    # temp or humidity hovers around d_ideal. For example, if d_curr is 71 F then
    # the heater will turn off, then turn on again if d_curr falls to 69 F, only
    # to turn off when d_curr rises to 71 again.
    #As the min to max range for temp is 55 F to 100 F, and humidity is
    # 50% to 100%, the same ideal range will be used for both:
    # 65 %/F to 80 %/F
    h_ideal = 80
    m_ideal = 70
    l_ideal = 65
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    
    #Get the current status of the heater/humidifier
    status = GPIO.input(pin)
    
    #If the device (heater/humidifier) is on
    if status:
        #if the current temp/hum is at or above the higher end of the range
        print("Current temp/hum is higher than ideal")
        if d_curr >= h_ideal:
            #Turn the heater/humidifier off
            GPIO.output(pin, 0)
            #If the current temp/hum is above max value, send an alert
            #if d_curr >= d_max:
                #print("Alert! Temperature/Humidity is too high.")
            #if verb is True:
                #print("Heater/Humidifier has been turned off.")
        else:
            print("Current temp/hum within ideal range")
                
    #if the heater/humidifier is off
    elif not status:
        #if the current temp/hum is below the lower end of the range
        if d_curr < l_ideal:
            print("Current temp/hum is lower than ideal")
            #turn the heater/humidifier on
            GPIO.output(pin, 1)
            #if temp/hum is below minimum, send an alert
            #if d_curr < d_min:
                #print("Alert! Temperature/Humiditiy is too low.")
            #if verb is True:
                #print("Heater/Humidifier has been turned on.")
        else:
            print("Current temp/hum within ideal range.")
    else:
        #For debugging purposes
        print("device boolean is NULL")
    GPIO.cleanup()
    return


def check_co2(max_co2, min_co2, curr_co2, pin, verb):
    
    h_ideal = 1800
    m_ideal = 1500
    l_ideal = 1300
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    
    #Get the current status of the vent fan
    status = GPIO.input(pin)
    
    #If the vent van is off
    if not status:
        #if the current co2 is at or above the higher end of the range
        print("Current Co2 is higher than ideal")
        if curr_co2 >= h_ideal:
            #Turn the fan on
            GPIO.output(pin, 1)
            #If the current co2 is above max value, send an alert
            #if curr_co2 >= d_max:
                #print("Alert! Co2 is too high.")
            #if verb is True:
                #print("Fan has been turned on.")
        else:
            print("Current co2 within ideal range")
                
    #if the vent fan is on
    elif status:
        #if the current co2 is below the lower end of the range
        if curr_co2 < l_ideal:
            print("Current co2 is lower than ideal")
            #turn the fan off
            GPIO.output(pin, 0)
            #if co2 is below minimum, send an alert
            if d_curr < d_min:
                print("Alert! Co2 is too low.")
            if verb is True:
                print("Van has been turned off.")
        else:
            print("Current co2 within ideal range.")
    else:
        #For debugging purposes
        print("device boolean is NULL")
    GPIO.cleanup()
    return

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
    min_temp = 55
    heat_pin = 16
    
    max_hum = 100
    min_hum = 50
    hum_pin = 20
    
    max_co2 = 2000
    ideal_co2 = 1500
    min_co2 = 1000
    vent_pin = 21
    
    #Check Temperature and control heater
    check_data(max_temp, min_temp, curr_temp, heat_pin, verb)
    #Check humidiity and control humidifier
    check_data(max_hum, min_hum, curr_hum, hum_pin, verb)
    #Check CO2
    check_co2(max_co2, min_co2, curr_co2, vent_pin, verb)
    #Check light
        #breeding_light(time?)

def init():
    #first time initialization code
    print("Initializing relays...")
    pin_list = [16, 20, 21, 25]
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_list, GPIO.OUT)
    GPIO.output(pin_list, GPIO.LOW)
    print("Initializing completed.")
    GPIO.cleanup()
    return
    
if __name__ == '__main__':
    pass
else:
    init()
