#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711

try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    dt_num = int(input("Enter DT pin number: "))
    sck_num = int(input("Enter SCK pin number: "))
    hx = HX711(dout_pin=dt_num, pd_sck_pin=sck_num)
#    hx = HX711(dout_pin=6, pd_sck_pin=5)

    print("\nReading data from scale. This will take about 15 seconds")
    offset = hx.get_raw_data_mean(readings=99)
    if offset:
        print('Raw data for tare:',offset)
    else:
        print('invalid data', offset)

    print("\ncurrent channel: " + str(hx.get_current_channel()))
    print("current gain: " + str(hx.get_current_gain_A()))
    hx.set_offset(offset, channel=hx.get_current_channel(), gain_A=hx.get_current_gain_A())

    input('\nPut known weight on the scale and then press Enter')
    reading = hx.get_data_mean()
    if reading:
        print('\nMean value from HX711 subtracted by offset:', reading)
        known_weight_grams = float(input('\nWrite how many grams it was and press Enter: '))
        print(known_weight_grams, 'grams')

        ratio = round(reading / known_weight_grams,3)
        hx.set_scale_ratio(ratio)
        print('Ratio is set to: ' + str(ratio))
    else:
        raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)


    print("\nCopy this String for configuration file:\n[" + str(dt_num) + "," + str(sck_num) + "," + str(offset) + "," + str(ratio) + "]")

    input('\nPress Enter to begin reading weight')
    print('Current weight on the scale in grams is: ')
    while True:
        print(hx.get_weight_mean(20), 'g')

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    GPIO.cleanup()
