#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int byteCounter= 0;
int valueRed = 0;
int valueGreen = 0;
int valueBlue = 0;
int valueWhite = 0;
int ledRed = 5;
int ledGreen = 6;
int ledBlue = 9;
int ledWhite = 10;

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  Serial.println("Ready!");
}

void loop() {
  //Serial.println(byteCounter);
  delay(100);
}

// callback for received data
void receiveData(int byteCount){

  while(Wire.available()) {
    //Serial.print(time);
    number = Wire.read();
    byteCounter++;
    
    //Serial.print("data received: ");
    //Serial.println(number);
    //Serial.print("\nByte Counter: ");
    //Serial.println(byteCounter);
    if (byteCounter == 1) {
      //Serial.print("Red:");
      valueRed = number;
    } else  if (byteCounter == 2) {
      //Serial.print("Red:");
      valueGreen = number;
    } else if (byteCounter == 3) {
      //Serial.print("Red:");
      valueBlue = number;
    } else if (byteCounter >= 4) {
        
      valueWhite = number;
      Serial.print("Red: ");
      Serial.print(valueRed);
      analogWrite(ledRed, valueRed);
      
      Serial.print(" Green: ");
      Serial.print(valueGreen);
      analogWrite(ledGreen, valueGreen);
      
      Serial.print(" Blue: ");
      Serial.print(valueBlue);
      analogWrite(ledBlue, valueBlue);
      
      Serial.print(" White: ");
      Serial.print(valueWhite);
      analogWrite(ledWhite, valueWhite);
      
      Serial.print("\n");
      byteCounter = 0;
    }
  }
  
}

// callback for sending data
void sendData(){
  Wire.write(number);
} 
