#!/usr/bin/python

# I put this script together to allow my Raspberry Pi to act as a color server for my Arduino Cheerlights tree. The XBee module is connected to the 3.3V, RX, and TX pins on the Pi's GPIO (http://baldwisdom.com/preparing-for-a-la-mode-raspberry-pi-and-arduino/) and the console was disabled (http://www.irrational.net/2012/04/19/using-the-raspberry-pis-serial-port/). I have the script set to run on boot (http://elinux.org/RPi_Email_IP_On_Boot_Debian).

import serial, scrapelib, json, time

def sendCheerlightsColor():
        try:
                cheerlights = json.loads(s.urlopen('http://api.thingspeak.com/channels/1417/field/1/last.json'))
                print 'The Cheerlights color was {0} at {1}.'.format(cheerlights['field1'],time.strftime("%H:%M:%S", time.localtime()))
                ser.write(cheerlights['field1'])
                ser.write(",")
        except:
                print 'Error in sendCheerlightsColor'

if __name__ == '__main__':
        s = scrapelib.Scraper(requests_per_minute=5, follow_robots=True)
        ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
        print ser                
        while True:
                try:
                        if ser.isOpen() == 0:
                                print 'Re-opening a serial connection'
                                ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
                        incoming = ser.readline()
                        if incoming[:len(incoming)-2] == 'CheerlightsColor':
                                print 'Send Color Command Received'
                                sendCheerlightsColor()
                        elif len(incoming) > 0:
                                incoming = incoming[:len(incoming)-2]
                                print 'The tree acknowledges {0}.'.format(incoming)
                        incoming = ''
                except:
                        print 'Error in main'
                time.sleep(5)