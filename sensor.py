#--------------------------------------------------------------------
# File name: sensor.py
# Author(s): Jennika Haining (jmh1592@rit.edu), Josh Noble (jtn6092@rit.edu)
# Date: 27 October 2020
# Project: MSD P21422 Black Soldier Fly Composting Smart Shed
# Purpose: To collect environmental data from temperature, humidity,
#          and co2 sensors for monitoring purposes
# Notes:
#       Indoor sensor: DATA = 16 (GPIO 24), SCK = 18 (GPIO 23), VDD = 3.5V
#       Outdoor sensor: DATA = 15 (GPIO 22), SCK = 13 (GPIO 27), VDD = 3.5V
#       Co2 sensor: SDA = 3 (GPIO SDA), SCL = 5 (GPIO SCL)
#
# To-Do: 
#--------------------------------------------------------------------

from pi_sht1x import SHT1x
import RPi.GPIO as GPIO
import board
import serial
import time

def c_to_f(temp_c):
    #Convert Celcius to Fahrenheit and round to 2 decimal places
    temp_f = round(((temp_c * 9/5) + 32), 2)
    return temp_f

def sht_indoor_sensor(in_temp_f, in_temp_c, in_hum, verb):
    #Get readings from indoor SHT1 sensor
    with SHT1x(24, 23, gpio_mode=GPIO.BCM) as sensor:
        in_temp_c = sensor.read_temperature()
        in_temp_f = sensor.read_temperature()
        in_hum = sensor.read_humidity(in_temp_c)
        sensor.calculate_dew_point(in_temp_c, in_hum)
        in_temp_f = c_to_f(in_temp_f)
        
        if verb:
            print('Indoor readings:\n', sensor)
            
    return in_temp_f, in_temp_c, in_hum


def sht_outdoor_sensor(out_temp_f, out_temp_c, out_hum, verb):
    #Get readings from outdoor SHT1 Sensor
    with SHT1x(22, 27, gpio_mode=GPIO.BCM) as sensor:
        out_temp_c = sensor.read_temperature()
        out_temp_f = sensor.read_temperature()
        out_hum = sensor.read_humidity(out_temp_c)
        sensor.calculate_dew_point(out_temp_c, out_hum)
        out_temp_f = c_to_f(out_temp_f)
        
        if verb:
            print('Outdoor readings:\n', sensor)
        
    return out_temp_f, out_temp_c, out_hum


def co2_sensor(verb):
    #Get the readings from the Co2 sensor
    #mult = 0 # 20% sensors requires a multiplier
    ser = serial.Serial("/dev/serial0")
#     ser.write(('M 4\r\n').encode())
#     ser.write(('K 2\r\n').encode())
    ser.flushInput()
    time.sleep(1)
    
    ser.write(str.encode("Z\r\n"))
    resp = ser.read(10)
    resp = resp[:8]
    flt = resp[2:]

    fltCo2 = float((resp[2:]).strip())
    #Print the readings,
    if verb:
        print("CO2 PPM = ", fltCo2)
        print("\n")
        
    return fltCo2

def sensor(in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2, verb):
 
    in_temp_f, in_temp_c, in_hum = sht_indoor_sensor(in_temp_f, in_temp_c, in_hum, verb)
    out_temp_f, out_temp_c, out_hum = sht_outdoor_sensor(out_temp_f, out_temp_c, out_hum, verb)
    co2 = co2_sensor(verb)
            
    return in_temp_f, in_temp_c, out_temp_f, out_temp_c, in_hum, out_hum, co2