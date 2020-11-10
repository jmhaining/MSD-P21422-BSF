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

def check_data(d_max, d_min, d_curr, pin, device, verb):
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
    
    #If the device (heater/humidifier) is on
    if device is True:
        #if the current temp/hum is at or above the higher end of the range
        if d_curr >= h_ideal:
            #Turn the heater/humidifier off
            GPIO.setmode(pin, 0)
            #If the current temp/hum is above max value, send an alert
            if d_curr >= d_max:
                print("Alert! Temperature/Humidity is too high.")
            if verb is True:
                print("Heater/Humidifier has been turned off.")
                
    #if the heater/humidifier is off
    elif device is False:
        #if the current temp/hum is below the lower end of the range
        if d_curr < l_ideal:
            #turn the heater/humidifier off
            GPIO.setmode(pin, 1)
            #if temp/hum is below minimum, send an alert
            if d_curr < d_min:
                print("Alert! Temperature/Humiditiy is too low.")
            if verb is True:
                print("Heater/Humidifier has been turned on.")
    else:
        #For debugging purposes
        print("device boolean is NULL")
    return


#def check_co2(max_co2, min_co2, ideal_co2, curr_co2, vent_pin, vent, verb):
    #if curr_co2 >= ideal_co2 && !vent
        #GPIO.output(vent_pin, 1)
        #open vent
    #if curr_co2 < ideal_co2 - 250 && vent
        #GPIO.output(vent_pin, 0)
        #close vent
    #if curr_co2 <= min_co2 || curr_co2 >= max_co3
        #send alert
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
    min_temp = 55
    heat_pin = 16
    #heater = GPIO.input(heat_pin)
    
    max_hum = 100
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
        #check_data(max_temp, min_temp, curr_temp, heat_pin, heater, verb)
    #Check Humidity
        #check_data(max_hum, min_hum, curr_hum, hum_pin, humidifier, verb)
    #Check CO2
        #def check_co2(max_co2, min_co2, ideal_co2, curr_co2, vent_pin, vent, verb)
    #Check light
        #breeding_light(time?)

def init():
    GPIO.setmode(GPIO.BCM)
    #first time initialization code
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    return
##    
##if __name__ == '__main__':
##    main()
##else:
##    init()