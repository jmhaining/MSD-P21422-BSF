#--------------------------------------------------------------------
# File name: main.py
# Author(s): Jennika Haining (jmh1592@rit.edu), Josh Noble (jtn6092@rit.edu)
# Date: 13 October 2020
# Project: MSD P21422 Black Soldier Fly Composting Smart Shed
# Purpose: To output environmental data to CSV file for analysis
# Notes:
#       Readings file: Readings.csv
#
# To-Do: 
#        Include relay code to control heater, humidifier, etc.
#--------------------------------------------------------------------

from datetime import date
from os import path
import RPi.GPIO as GPIO
#import relay
import sensor
import sys
import csv
import time
import board
import busio
import adafruit_ccs811

def cur_date_time(today, now, verb):
    #Get date and time
    today = date.strftime(date.today(), '%m/%d/%y')
    now = time.strftime('%I:%M:%S%p', time.localtime())
    
    if verb:
        print('Current Date:', today, now)
        
    return today, now
          

def write_to_csv(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, tvoc, today, now):
    #Append to csv file with collected data
    with open('/home/pi/Desktop/Readings.csv', mode='a') as data_file:
        data = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        data.writerow([today, now, out_temp_c, out_temp_f, in_temp_c, in_temp_f, out_hum, in_hum, co2, tvoc])
        data_file.close()
    return


def main(argv):
    #If True, data will print to shell as well as write to file
    #If False, data will only write to file
    verb = ''
    if len(sys.argv) == 2:
        if sys.argv[1] == '-v' or sys.argv[1] == '-verb' or sys.argv[1] == '-verbose':
            verb = True
        else:
            print("Invalid argument. Valid argument(s): -v[erbose]")
    else:
        verb = False
    
    #relay.init()
    #Intialize co2 sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    ccs811 = adafruit_ccs811.CCS811(i2c)
    
    #Data variables initialization
    in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, tvoc = 0, 0, 0, 0, 0, 0, 0, 0
    today, now = '0', '0'
        
    #If the csv file does not exist, initialize it
    if not path.exists('/home/pi/Desktop/Readings.csv'):
        with open('/home/pi/Desktop/Readings.csv', mode='w') as data_file:
            data = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            data.writerow(['DATE', 'TIME', 'OUTDOOR TEMP C', 'OUTDOOR TEMP F', 'INDOOR TEMP C', 'INDOOR TEMP F', 'OUTDOOR HUMIDITY', 'INDOOR HUMIDITY', 'CO2', 'TVOC'])
            data_file.close
    else:
        pass
    
    while True:
        if not ccs811.data_ready:
            pass
        else:
            today, now = cur_date_time(today, now, verb)
            in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, tvoc = \
                       sensor.sensor(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, ccs811, co2, tvoc, verb)
            write_to_csv(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, tvoc, today, now)
            #relay.relay(in_temp_f, in_hum, co2, verb)
            
            #sleep in seconds. 60 = 1 minute, 300 = 5 minutes, 1800 = 30 minutes
            time.sleep(1800.0)
    return

if __name__ == '__main__':
    main(sys.argv[0:])
    #main()
