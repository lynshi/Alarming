/* Arduino Alarm Clock
 * Description: The Sketch uses Serial Communcation to run an alarm clock. 
 * This is intended to act as an ioT Device. 
 * Author: Skyler Shi, Anirudh Pal
 */
 
 // Import Libraries
#include "pitches.h" // Used to play Tones
#include <Wire.h> // Used for i2c Communication
#include "rgb_lcd.h" // Library to Interface with LCD (Should be replaced)

// Pin Defination
const char BP = 6; // Buzzer
const char VP = A0; // Vibration
// Global Variables
rgb_lcd lcd; // LCD Object
const int threshold = 900; // Vibration Threshold
const char colorR = 255; // Red Value
const char colorG = 255; // Green Value
const char colorB = 255; // Blue Value
const int melody[] = {NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4}; // Melody Defination
const char noteDurations[] = {4, 8, 8, 4, 4, 4, 4, 4}; // Melody Duration
char alarm = 0; // Alarm
int time_hour1; // Hours
int time_hour2;
int time_min1; // Mins
int time_min2;
String message; // Message
String com; // Pi Transmition

/* The following setups:
 * 1.Serial Communication with Pi
 * 2.i2c with LCD
 * 3.Set Buzzer Output
 * 4.Set Vibration Input
 */
void setup() {
  pinMode(A0,INPUT);
  // Start Talking to Pi
  Serial.begin(9600);
  // Start Talking to LCD
  lcd.begin(16, 2);
  // Set Color (Remove Later)
  lcd.setRGB(colorR, colorG, colorB);
  // Set Buzzer Output
  pinMode(BP, OUTPUT);
  // Delay
  delay(1000);
}

/* The following loops:
 * 1.Communication
 * 2.Updates Alarm & Display
 */
void loop() {
  parseData();
}

/* Plays the Alarm & Flashes Screen*/
void playAlarm(){
  // Control Loop
  while(1) {
    // Melody Loop
    for (int thisNote = 0; thisNote < 8; thisNote++) {
      // Determine Note Duration
      int noteDuration = 1000 / noteDurations[thisNote];
      // Push Tone & LCD RGB
      lcd.setRGB(colorR, 0, 0);
      tone(BP, melody[thisNote], noteDuration);
      // Pause Duration & LCD RGB
      int pauseBetweenNotes = noteDuration * 1.30*.5;
      delay(pauseBetweenNotes);
      lcd.setRGB(0, colorG, 0);
      delay(pauseBetweenNotes);
      // Stop Note
      noTone(BP);
    }
    // Break Statement
    if(analogRead(VP) > threshold)
      break;
  }
  // Turn White
  lcd.setRGB(colorR, colorG, colorB);
}

/* Parse Serial Data */
void parseData() {
  // Serial Data Available
  if(Serial.available()) {
    // Catch Data
    com = Serial.readStringUntil('\n');
    // Parse Data
    time_hour1 = (com.substring(0,1)).toInt();
    time_hour2 = (com.substring(1,2)).toInt();
    time_min1 = (com.substring(2,3)).toInt();
    time_min2 = (com.substring(3,4)).toInt();
    alarm = (com.substring(4,5)).toInt();
    message = com.substring(5, com.indexOf('\n'));
    /* Test Print
    Serial.print("Time: ");
    Serial.print(time_hour);
    Serial.print(":");
    Serial.print(time_min);
    Serial.print(" ");
    Serial.print(alarm);
    Serial.print(" ");
    Serial.println(message);
    */
    // Display Clock & Alarm
    display();
    if(alarm == 1) {
      playAlarm();
      alarm = 0;
    }
  }
}

/* Used to Display Clock */
void display() {
  // Display Clock & Message LCD
  lcd.setCursor(0, 0);
  lcd.clear();
  lcd.print(0x0);
  lcd.print(time_hour2);
  lcd.print(":");
  lcd.print(time_min1);
  lcd.print(time_min2);
  lcd.setCursor(0,1);
  lcd.print(message);
}
