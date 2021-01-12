# SMS_IoT
## Personal Communication Service final project
Using SMS to control and monitor a smart garden system built with IoT devices
* Water the plant when sending an SMS containing “water”
* Return the sensor values when sending a SMS containing “sensor”, including brightness, humidity and temperature in the room, soil moisture and total watering times.

### Requirements
* a **Twilio** account and number
* Arduino Uno
* Raspberry Pi
* sensors: soil moisture, light, temperature and humidity sensor
* battery case
* water pump
* small fan

### Hardware
![alt text](https://github.com/105061210/SMS_IoT/blob/main/assets/pcs_final_1.jpg)


### Software
```
pip install twilio
pip install Flask
sudo wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
sudo unzip ngrok-stable-linux-arm.zip
```
Go to https://dashboard.ngrok.com/login in browser to log in / sign up
Click **Auth** and get Authtoken
```
./ngrok authtoken <the token depends on your account>
```
```
./ngrok http 5000
```
and configure the URL in Twilio account

### Result
By uploading src/pcs_final.ino to Arduino and running bot.py on Raspberry Pi
```
python bot.py
```
* demo video: https://drive.google.com/file/d/1zly6OD56tLU_YGzDxqX4LgoZecO9N_bo/view?usp=sharing

![alt text](https://github.com/105061210/SMS_IoT/blob/main/assets/pcs_final.jpeg)







