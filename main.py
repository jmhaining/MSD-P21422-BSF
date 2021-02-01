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
from dbox_upload import upload
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError


# Dropbox access token - set to never expire
TOKEN = 'sl.AqesqhFtrGLExOEaCZfVqqo91tKyymK3fm94EA0Wwo1HhBlMU8-aHEbUrovvIsZBz4RL7bWF4xhw_sxW3x9LNmTvBk2KQJqb0BMsFlONRsrKo8AFL4paj8IStc-wm4u1q5_WTuq2gDg'

def cur_date_time(today, now, verb):
    #Get date and time
    today = date.strftime(date.today(), '%Y/%m/%d')
    now = time.strftime('%I:%M:%S%p', time.localtime())
    
    if verb:
        print('Current Date:', today, now)
        
    return today, now
          

def write_to_csv(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, today, now, fpath):
    #If the file does not exist, create it, add headers, and add first line of data
    if not path.exists(fpath):
        with open(fpath, mode='a') as data_file:
            data = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            data.writerow(['DATE', 'TIME', 'OUTDOOR TEMP C', 'OUTDOOR TEMP F', 'INDOOR TEMP C', 'INDOOR TEMP F', 'OUTDOOR HUMIDITY', 'INDOOR HUMIDITY', 'CO2'])
            data.writerow([today, now, out_temp_c, out_temp_f, in_temp_c, in_temp_f, out_hum, in_hum, co2])
            data_file.close
    #Otherwise, just append new line of data
    else:
        with open(fpath, mode='a') as data_file:
            data = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            data.writerow([today, now, out_temp_c, out_temp_f, in_temp_c, in_temp_f, out_hum, in_hum, co2])
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
    
    #Initialize file path for readings
    fpath = "/home/pi/MSD-P21422-BSF/Readings/"
    
    #Initialize data variables
    in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2 = 0, 0, 0, 0, 0, 0, 0
    today, now = '0', '0'

    # Initialize Dropbox link; check for access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token."
	        "Go to https://www.dropbox.com/developers/apps. Generate"
		    "a token in app settings and add it to line 24")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(TOKEN)

    # Check that Dropbox access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an"
		 "access token from the app console on the web.")
    
    while True:
        today, now = cur_date_time(today, now, verb)
        file_name = date.strftime(date.today(), '%Y%m%d.csv')
        full_path = fpath + file_name
        in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2 = \
                    sensor.sensor(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, verb)
        write_to_csv(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, today, now, full_path)
        #relay.relay(in_temp_f, in_hum, co2, verb)
            

        # Upload the file to Dropbox
        print("Uploading the file...")
        upload(file_name, full_path)

        #sleep in seconds. 60 = 1 minute, 300 = 5 minutes, 1800 = 30 minutes
        time.sleep(1800.0)
    return

if __name__ == '__main__':
    main(sys.argv[0:])
    #main()