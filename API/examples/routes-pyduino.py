from flask import Flask, render_template, request, redirect, url_for
from pyduino import *
import time

app = Flask(__name__)

# initialize connection to Arduino
# if your arduino was running on a serial port other than '/dev/ttyACM0/'
# declare: a = Arduino(serial_port='/dev/ttyXXXX')
a = Arduino() 
time.sleep(3)

# declare the pins we're using
LED_PIN = 3
ANALOG_PIN = 0

# initialize the digital pin as output

print('Arduino initialized')

# we are able to make 2 different requests on our webpage
# GET = we just type in the url
# POST = some sort of form submission like a button
@app.route('/turn-on')
def turn_on():

    print('TURN ON')
    
    # turn on LED on arduino
    a.digital_write(LED_PIN, 1)
    
    # read in analog value from photoresistor
    readval = a.analog_read(ANALOG_PIN)

    # the default page to display will be our template with our template variables
    return {
        "success": True,
        "message": "LED ON"
    }

@app.route('/turn-off')
def turn_off():

    print('TURN OFF')

    # turn off LED on arduino
    a.digital_write(LED_PIN,0)
    
    # read in analog value from photoresistor
    readval = a.analog_read(ANALOG_PIN)

    # the default page to display will be our template with our template variables
    return {
        "success": True,
        "message": "LED OFF"
    }

if __name__ == "__main__":

    # lets launch our webpage!
    # do 0.0.0.0 so that we can log into this webpage
    # using another computer on the same network later
    app.run(debug=True)