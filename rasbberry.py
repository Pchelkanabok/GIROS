import time
import sys
import pandas as pd
import psycopg2

EMULATE_HX711 = False
connection = psycopg2.connect(host="192.168.16.82", port="2669", password="nast", dbname="GIROS", user="Nast")
connection.autocommit = True
box_id = 1

referenceUnit = 492.0903

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711


def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()

hx = HX711(24, 25)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1 gram is 184000 / 2000 = 92.
# hx.set_reference_unit(113)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")



while True:
    try:
        val = 0

        val = hx.get_weight(5)

        if (len(pd.read_sql('Select * from "history_purch", "history_place" '
                            'where history_place.id_place = history_purch.id_place '
                            'and id_box = 1 and mass_prev is null', connection)) == 1):
            str_ = "update public.history_purch set mass_prev =" + str(val) + \
                   "where id_place = (select id_place from history_place where id_box = " + str(box_id) + \
                   "and data_time_stop is NULL) and mass_prev is null"
            connection.cursor().execute(str_)
            print("zapolnen")

        if len(pd.read_sql('select * from history_purch '
                           'where id_place = (select id_place from history_place where id_box = 1 and data_time_stop is NULL) '
                           'and mass_hbc is null and time_close is not null', connection)) == 1:
            str_ = 'update public.history_purch set mass_hbc = ' + str(val) + \
                   ' where id_place = (select id_place from history_place where id_box = 1 and data_time_stop is NULL) ' \
                   'and mass_hbc is null and time_close is not null'
            connection.cursor().execute(str_)
            print('zapisal HBC')

        # print(val / referenceUnit, 'grams')
        print(val, 'units')

        # To get weight from both channels (if you have load cells hooked up
        # to both channel A and B), do something like this
        # val_A = hx.get_weight_A(5)
        # val_B = hx.get_weight_B(5)
        # print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()