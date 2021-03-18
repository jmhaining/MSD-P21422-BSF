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
import relay
import sensor
import sys
import csv
import time
import board
from dbox_upload import upload
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import urllib.request

def get_token():
    file = open("/home/pi/MSD-P21422-BSF/db_token.txt", mode='r')
    token = file.readline()
    file.close()
    return token

def cur_date_time(today, now, verb):
    #Get date and time
    today = date.strftime(date.today(), '%Y/%m/%d')
    now = time.strftime('%I:%M:%S%p', time.localtime())
    
    if verb:
        print('Current Date:', today, now)
        
    return today, now
          

def write_to_csv(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, today, now, heat_stat, hum_stat, fan_stat, light_stat, fpath):
    #If the file does not exist, create it, add headers, and add first line of data
    if not path.exists(fpath):
        with open(fpath, mode='a') as data_file:
            data = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            data.writerow(['DATE', 'TIME', 'OUTDOOR TEMP C', 'OUTDOOR TEMP F', 'INDOOR TEMP C', 'INDOOR TEMP F', 'OUTDOOR HUMIDITY', 'INDOOR HUMIDITY', 'CO2', 'HEAT STAT', 'HUM STAT', 'FAN STAT', 'LIGHT STAT'])
            data.writerow([today, now, out_temp_c, out_temp_f, in_temp_c, in_temp_f, out_hum, in_hum, co2, heat_stat, hum_stat, fan_stat, light_stat])
            data_file.close
    #Otherwise, just append new line of data
    else:
        with open(fpath, mode='a') as data_file:
            data = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            data.writerow([today, now, out_temp_c, out_temp_f, in_temp_c, in_temp_f, out_hum, in_hum, co2, heat_stat, hum_stat, fan_stat, light_stat])
            data_file.close()
    return


def db_access():
    # Initialize Dropbox link; check for access token
    token = get_token()
    if (len(token) == 0):
        # edited 3-9 JN
        # sys.exit("ERROR: Looks like the Dropbox access token is missing or expired."
        print("ERROR: Looks like the Dropbox access token is missing or expired." 
            "Go to https://www.dropbox.com/developers/apps. Login and click on the" 
            "MSD-21422 app. Go to settings, generate a new access code and copy it"
            "in line 30")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    # edited 3-9 JN
    try:
        dbx = dropbox.Dropbox(token)
    except:
        pass

    # Check that Dropbox access token is valid
    try:
        dbx.users_get_current_account()
        db_connect = True
    except AuthError as err:
        #sys.exit("ERROR: Invalid access token; try re-generating an"
		#"access token from the app console on the web.")
        # edited 3-9 JN
        print("ERROR: Invalid access token; try re-generating an"
		 "access token from the app console on the web.")
        db_connect = False
    return dbx, db_connect


def check_connection(host='http://google.com'):
    #Check is there is an internet connection by testing connection to google
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


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

    dbx = 0
    db_connect = False
    
    #Check if connected to internet
    if check_connection():
        #If connected to internet, establish dropbox connection
        dbx, db_connect = db_access()
    
    while True:
        today, now = cur_date_time(today, now, verb)
        file_name = date.strftime(date.today(), '%Y%m%d.csv')
        full_path = fpath + file_name
        in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2 = \
                    sensor.sensor(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, verb)
        heat_stat, hum_stat, fan_stat, light_stat = relay.relay(in_temp_f, in_hum, co2, verb)
        write_to_csv(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, today, now, heat_stat, hum_stat, fan_stat, light_stat, full_path)

        # Check the internet connection
        if check_connection():
            #If connected to internet but not dropbox
            if db_connect == False:
                #Establish dropbox connection
                dbx, db_connect = db_access()
            
            #If connected to internet and to dropbox
            if db_connect == True:
                #Upload file to dropbox
                print("Uploading the file...")
                upload('/' + file_name, full_path, dbx)
                print("Upload successful")
        #TO-DO:
            #If connection is down for more than a day, add a case to upload files that were missed
        
        #sleep in seconds. 60 = 1 minute, 300 = 5 minutes, 1800 = 30 minutes
        time.sleep(599.0)
    return

if __name__ == '__main__':
    main(sys.argv[0:])
    #main()
