from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from serial import Serial
import sys
import threading
import time
import picamera

ser = Serial('/dev/ttyACM0', 9600, timeout= 0.5 )
app = Flask(__name__)


class RxThread(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.cnt = 0
        self.light = 0 
        self.temper = 0 
        self.humid = 0
        self.soil = 0

        
    def run(self):
    
        tStart = time.time()
        while True:
            while self.ser.inWaiting():
                
                
                res = ser.readline().decode('utf8')[:-2]
                print(res)

                if "water" in res:
                    end = res.find("|")
                    self.cnt  = int(res[15:end])
                elif "Light" in res:
                    end = res.find("l")
                    self.light = float(res[6:end])
                elif "Soil" in res:
                    self.soil = int(res[5:])

                elif "Humid" in res:
                    end = res.find("%")
                    self.humid = float(res[9:end])
                elif "Temper" in res:
                    end = res.find("*C")
                    self.temper = float(res[12:end])
                else:
                    pass
                tEnd = time.time()
                with open("sensor.txt", "w") as f:
                    f.writelines("Light:" + str(self.light) + " Soil:" + str(self.soil) + " Temperature:" + str(self.temper) + " Himidity:" + str(self.humid) + " @watering times:" + str(self.cnt))
                
                
    def resume(self):
        self._running = True
        
    def stop(self):
        self._running = False


def both():
    rx = RxThread(ser)
    rx.start()


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    
    if 'water' in incoming_msg:
        trans = 'W' + "\n"
        ser.write(trans.encode())
        quote = "Watering!!! "
        msg.body(quote)
        responded = True
    if 'sensor' in incoming_msg:
        #cam = picamera.PiCamera()
        #cam.vflip = True
        #cam.hflip = True
        #cam.capture('images/lab.jpg')
        #cam.close()
        quote = "Info: "
        with open("sensor.txt", "r") as ff:
            quote += str(ff.readlines())
        msg.body(quote)
        #msg.media("images/lab.jpg")
        responded = True
    if not responded:
        msg.body('I only know anything, sorry!')
    return str(resp)

if __name__ == "__main__":
    both()
    app.run(debug=True)
    

