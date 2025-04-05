// SPDX-FileCopyrightText: Copyright 2025 Alexander Kirillov <shurik179@gmail.com>
// SPDX-License-Identifier: MIT
// partly based on https://github.com/SpenceKonde/megaTinyCore/blob/master/megaavr/libraries/Wire/examples/register_model/register_model.ino

#include <Wire.h>
#include <EEPROM.h>

//firmware version 
#define FW_MINOR 8
#define FW_MAJOR 0
#define PIN_ENABLE PIN_PB3
#define PIN_ADDR PIN_PC2 //for changing I2C address

#define NUM_SENSORS 6
#define NUM_REGISTERS 32 //size of register bank, in bytes
#define SLAVE_ADDRESS 0x11
#define MODE_OFF 0
#define MODE_ON 1
#define MODE_CAL 2
#define MODE_CAL_END 3
#define LINEMODE_BLACKONWHITE 0
#define LINEMODE_WHITEONBLACK 1 
volatile uint8_t DevRegister[NUM_REGISTERS]; //register bank
volatile uint8_t WirePointer = 0;
volatile uint8_t ModeChange = 0; //to signal that mode had changed
uint8_t mode = MODE_ON;

//register definitions
#define REG_WHOAMI     0
#define REG_MODE       1
#define REG_LINE_MODE  2
#define REG_FW_MINOR   3
#define REG_FW_MAJOR   4
#define REG_STATUS     5 //for debugging
#define REG_SENSOR_RAW 6 //start of raw readings block. 
                         //each sensor is recorded as two bytes; e.g. raw reading of sensro 0 is 
                         // at registers 6 (low byte) and 7(high byte) 
#define REG_SENSOR_CAL 18 //start of calibrated readings block. 
                         //each sensor is recorded as two bytes; e.g. calibrated reading of sensor 0 is 
                         // at registers 18 (low byte) and 19(high byte) 
#define REG_SENSOR_DIGITAL 30 // byte containing sensor readings in digital (0/1) form, 1 bit for sensor
                              // least significant bit is sensor 0                          
#define REG_LINE_POS 31 //line position as uint8_t, ranges 0-100                               

uint8_t SensorPins[NUM_SENSORS] = { PIN_PB4, PIN_PB5, PIN_PA7, PIN_PA6, PIN_PA5, PIN_PA4 };
uint16_t BlackCalibration[NUM_SENSORS] = {120,120,120,120,120,120};
uint16_t WhiteCalibration[NUM_SENSORS] = {980,980,980, 980, 980,980};

uint8_t s; // temporary, sensor index





void setup() {
    pinMode(PIN_ADDR, INPUT_PULLUP);
    pinMode(PIN_ENABLE, OUTPUT);
    digitalWrite(PIN_ENABLE, HIGH);
    if (digitalRead(PIN_ADDR)) { //if high, use default address
        Wire.begin(SLAVE_ADDRESS);       
    } else { //solder bridge was closed - use next 
        Wire.begin(SLAVE_ADDRESS+1);             
    }
    Wire.onReceive(receiveHandler);
    Wire.onRequest(requestHandler);
    DevRegister[REG_WHOAMI] = SLAVE_ADDRESS;
    DevRegister[REG_FW_MINOR] = FW_MINOR;
    DevRegister[REG_FW_MAJOR] = FW_MAJOR;
    DevRegister[REG_MODE] = MODE_ON;
    DevRegister[REG_LINE_MODE] = LINEMODE_BLACKONWHITE;
    //get calibration data from eeprom
    read_calibration();
}

void loop() {
    //check if the mode had been changed; if so, enable/disable the sensors
    if (ModeChange) {
        ModeChange = 0;
        mode = DevRegister[REG_MODE];
        if (mode == MODE_OFF) {
            digitalWrite(PIN_ENABLE, LOW);
        } else {
            digitalWrite(PIN_ENABLE, HIGH);
        }
        if (mode == MODE_CAL) { //starting calibration
            //reset calibrartion data 
            for (s =0; s<NUM_SENSORS; s++){
                BlackCalibration[s]=0;
                WhiteCalibration[s]=1023;
            }
        } else if (mode == MODE_CAL_END) { //ending calibration
            //save calibration data to eeprom  
            save_calibration();
            //automatically switch to run mode 
            DevRegister[REG_MODE] = MODE_ON;
            mode = MODE_ON;
        }
    }
    //if (mode == MODE_OFF) return; //no need to measure anything 
    //otherwise, get sensor values; also compute the average, for line position 
    uint16_t pos = 0;
    uint16_t total_weight = 0;
    uint16_t r,line_pos;
    for (s=0; s<NUM_SENSORS; s++){
        if (mode == MODE_CAL) {update_calibration(s);}
        else {
            r = update_value(s); //returns calibrated value 
            if (DevRegister[REG_LINE_MODE] == LINEMODE_BLACKONWHITE) {r=1023-r;}
            //computing the weighted average of sensor indexes, using reading as weight
            //will be used for line position 
            pos += s* r;
            total_weight += r; 
        }
    }
    //now, get the line position 
    if (total_weight) { //just in case, to make sure we are not dividing by 0
        line_pos = (pos*20)/total_weight; //ranges between 0 - (NUM_SENSORS-1)*20, i.e. 0-100
        DevRegister[REG_LINE_POS] = line_pos;
    }
}

void receiveHandler(int numbytes) {
    Wire.getBytesRead(); // reset count of bytes read. We don't do anything with it here, but a write is going to reset it to a new value.
    WirePointer = Wire.read(); 
    numbytes--; // we just read a byte, so we should decrement this.
    while (numbytes > 0) { // If numbytes was more than 1, we'll execute the below loop to write to the "registers".
        //the only writable registers are REG_MODE, REG_LINE_MODE, attempts to write to other registers will be ignored
        if  ((WirePointer == REG_MODE) || (WirePointer == REG_LINE_MODE)) {
            DevRegister[WirePointer] = Wire.read();
            ModeChange = 1;
        } else {
            //read byte and discard 
            Wire.read();
        }
        WirePointer++;          // increment the pointer.
        numbytes--;             // decrement remaining bytes.
    }
}


void requestHandler() {
    uint8_t i;
    // We will start reading from the pointer
    i = WirePointer;
    while (i< NUM_REGISTERS) {
        Wire.write(DevRegister[i]);
        i++;
        // "write" the whole array - but the master might only want one byte.
        // The slave doesn't know how much data the master will want yet.
        // and won't know until it's gotten all that it wants and has generated a stop condition.
    }
  
}

//Updates readings of sensor index s (normal mode)
//returns the reading as uint16_t
uint16_t  update_value(uint8_t s){
    uint16_t reading; 
    int32_t calReading;
    reading = 1023 - analogRead(SensorPins[s]); // so that black corresponds to 0, and white, to 1023
    DevRegister[REG_SENSOR_RAW + 2*s] = (uint8_t) reading; //low byte
    DevRegister[REG_SENSOR_RAW + 2*s+1] = (uint8_t)(reading>>8);     //high byte
    //now, do the calibrated ones
    
    calReading = 1023*((int32_t)reading - BlackCalibration[s]);
    calReading /= WhiteCalibration[s]- BlackCalibration[s];
    if (calReading < 0) calReading = 0;
    if (calReading > 1023) calReading = 1023;
    DevRegister[REG_SENSOR_CAL + 2*s  ] = (uint8_t) calReading; //low byte
    DevRegister[REG_SENSOR_CAL + 2*s+1] = (uint8_t) (calReading>>8);     //high byte
    //do the digital ones 
    if (calReading >= 512){
        //sensor s is white: set s-th bit
        DevRegister[REG_SENSOR_DIGITAL] |= (1<<s); 
    } else {
        //sensor s is black: unset s-th bit  
        DevRegister[REG_SENSOR_DIGITAL] &= (0b11111110<<s);             
    }
    return(calReading);
}

void update_calibration(uint8_t s){
    uint16_t reading; 
    reading = 1023 - analogRead(SensorPins[s]); // so that black corresponds to 0, and white, to 1023
    if (reading < BlackCalibration[s]) {
        BlackCalibration[s] = reading;
    }
    if (reading > WhiteCalibration[s]) {
        WhiteCalibration[s] = reading;
    }
}



// saves calibration data to eeprom
void save_calibration(){
    for (s = 0; s<NUM_SENSORS; s++){
        // each value takes 2 bytes, so 4 bytes per sensor: 2 for black value, 2 for white
        EEPROM.put(4*s,  BlackCalibration[s]);
        EEPROM.put(4*s+2,  WhiteCalibration[s]);
    }
    //for testing purposes:
    DevRegister[REG_STATUS] = (uint8_t) BlackCalibration[0];
}

//gets calibration data from eeprom
void read_calibration (){
    uint16_t white, black;
    for (s = 0; s<NUM_SENSORS; s++){
        // each value takes 2 bytes, so 4 bytes per sensor: 2 for black value, 2 for white
        EEPROM.get(4*s,  black);
        EEPROM.get(4*s+2,  white);
        if (white > 0  && white <= 1023) { //basic sanity check, to make sure eeprom has valid values
            BlackCalibration[s] = black;
            WhiteCalibration[s] = white;
        }
    }
}
