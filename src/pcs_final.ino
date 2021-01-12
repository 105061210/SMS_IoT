#include <DHT.h>        //teperature&humidity
#include <Wire.h>       //i2c

#define DHTPIN A1       // A1 for temperature & humidity
#define LiIN A2         // A2 for light sensor
#define wheelPin 3      // D3 for fan

#define DHTTYPE DHT22   // DHT 22  (AM2302)
DHT dht(DHTPIN, DHTTYPE);

bool toWater = false;        

void setup() {
  Serial.begin(9600); 
  pinMode(7,OUTPUT);          //繼電器的接腳
  pinMode(wheelPin, OUTPUT);  //風扇
  Wire.begin();
  dht.begin();
  
}

int cnt = 0;
void loop() {

  if (toWater){
    digitalWrite(7,LOW);  //澆水
    delay(100);
    cnt += 1;
    Serial.print("watering times: ");
    Serial.print(cnt);
    Serial.println("|");
    digitalWrite(7,HIGH); //不澆水
    toWater = false;
  }
  
  digitalWrite(7,HIGH);   //不澆水
  delay(3000);            //延遲時間，可自行調整
  
  int sensorValue = analogRead(A0); //土壤濕度感測器的接腳，讀取數值
  Serial.print("Soil:");
  Serial.println(sensorValue);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float l = analogRead(LiIN);
  if (t >= 19)
  {
      digitalWrite(wheelPin, HIGH);
  }
  else
  {
      digitalWrite(wheelPin, LOW);
  }
  
  if (isnan(t) || isnan(h)) 
  {
    Serial.print("Light:"); 
    Serial.println(l); 
  } 
  else 
  {
    Serial.print("Humidity:"); 
    Serial.print(h);
    Serial.println("%");
    Serial.print("Temperature:"); 
    Serial.print(t);
    Serial.println("*C");
    Serial.print("Light:");
    Serial.print(l); 
    Serial.println("l");
  }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();

    if (inChar == 'W') {
      toWater = true;
    }
    else if (inChar == '\n' & toWater == true){
      toWater = true;
    }
    else{
      toWater = false;
    }
     
  }
}
