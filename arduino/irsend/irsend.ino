#include <IRremote.h>
#include <SoftwareSerial.h>

IRsend irsend;
const int freq = 38;
String command;

  
const unsigned int ac_on_18_auto_cool[] PROGMEM = {8900,4500, 500,600, 500,600, 550,1700, 500,
600, 550,1700, 500,600, 550,600, 500,650, 500,600, 550,1700, 500,600, 550,550, 550,600, 
550,600, 500,1700, 550,1700, 500,600, 550,600, 500,600, 550,600, 500,600, 550,
600, 500,600, 550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,550, 
550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,550, 550,600, 550,
600, 500,600, 550,1700, 500,1750, 500,1700, 500,600, 550,600, 500,600, 550,600, 
500,1750, 500,600, 550,600, 500,600, 550,600, 500,600, 550,1700, 500,1700, 500,1750, 
500,600, 550,600, 500,600, 550,600, 500,1750, 500,600, 500,600, 550,600, 500};

const unsigned int ac_off[] PROGMEM = {8900,4500, 500,600, 500,600, 550,1700, 500,600, 550,600, 
500,600, 550,600, 500,600, 550,600, 550,1700, 500,600, 550,550, 550,600, 550,1700, 
500,600, 550,600, 500,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,550, 550,
600, 550,600, 500,600, 550,600, 550,550, 550,600, 550,550, 550,600, 550,600, 550,550, 
550,600, 550,550, 550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,1700, 500,
600, 550,1650, 550,600, 500,600, 550,600, 550,1700, 500,600, 550,600, 500,600, 550,600, 
500,600, 550,1700, 500,1750, 500,1700, 500,600, 550,600, 500,600, 550,600, 550,1650, 
550,600, 500,600, 550,600, 550};

const unsigned int ac_on[] PROGMEM = {8900,4500, 500,600, 500,600, 550,1700, 500,600, 550,1700, 
500,600, 550,600, 500,650, 500,600, 550,1700, 500,600, 550,600, 500,600, 550,1700, 500,600, 
550,600, 550,550, 550,600, 550,550, 550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,
550, 550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,600, 500,600, 550,600, 500,600, 
550,550, 550,600, 550,600, 500,650, 500,1700, 550,1650, 550,600, 500,1700, 550,600, 500,600, 
550,600, 550,1700, 500,600, 550,600, 500,600, 550,600, 500,600, 550,1700, 500,1700, 550,1700, 
500,600, 550,600, 500,600, 550,600, 550,1650, 550,600, 500,600, 550,600, 550};

const unsigned int  tv_on[] PROGMEM = {2700,850, 450,850, 500,400, 450,400, 1350,1250, 450,400, 
500,400, 450,400, 450,450, 450,400, 500,400, 450,450, 450,400, 450,450, 450,400, 450,
450, 900,400, 450,850, 500,400, 450};




void sendIR(int cod){
    switch (cod)
    {
        case (0):
            Serial.println("TV ON/OFF");
            irsend.sendRaw(tv_on, sizeof(tv_on) / sizeof(tv_on[0]), freq);  
            delay(100);
            break;
        case 2:
            Serial.println("AC ON");
            irsend.sendRaw(ac_on, sizeof(ac_on) / sizeof(ac_on[0]), freq);
            delay(100);
            break;
        case 3:
            Serial.println("AC OFF");
            irsend.sendRaw(ac_off, sizeof(ac_off) / sizeof(ac_off[0]), freq);
            delay(100);
            break;
        default:
            Serial.println("Unknown command");
            break;
    }
}


void setup(){
    // Open serial communications and wait for port to open:
    Serial.begin(57600);
    while (!Serial) continue;
    
}

void loop(){
    if(Serial.available() > 0){
        command = Serial.readString();
        Serial.println(command);
        sendIR(command.toInt());
    }
}
