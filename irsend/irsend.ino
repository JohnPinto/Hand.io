#include <IRremote.h>
#include <SoftwareSerial.h>
#include <ArduinoJson.h>

IRsend irsend;
const int freq = 38;
const size_t capacity = JSON_OBJECT_SIZE(1) + 10;
unsigned int code[39];
int i;

//String command;

  
/*unsigned int ac_on_18_auto_cool[] = {8900,4500, 500,600, 500,600, 550,1700, 500,
600, 550,1700, 500,600, 550,600, 500,650, 500,600, 550,1700, 500,600, 550,550, 550,600, 
550,600, 500,1700, 550,1700, 500,600, 550,600, 500,600, 550,600, 500,600, 550,
600, 500,600, 550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,550, 
550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,550, 550,600, 550,
600, 500,600, 550,1700, 500,1750, 500,1700, 500,600, 550,600, 500,600, 550,600, 
500,1750, 500,600, 550,600, 500,600, 550,600, 500,600, 550,1700, 500,1700, 500,1750, 
500,600, 550,600, 500,600, 550,600, 500,1750, 500,600, 500,600, 550,600, 500};

unsigned int ac_off[] = {8900,4500, 500,600, 500,600, 550,1700, 500,600, 550,600, 
500,600, 550,600, 500,600, 550,600, 550,1700, 500,600, 550,550, 550,600, 550,1700, 
500,600, 550,600, 500,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,550, 550,
600, 550,600, 500,600, 550,600, 550,550, 550,600, 550,550, 550,600, 550,600, 550,550, 
550,600, 550,550, 550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,1700, 500,
600, 550,1650, 550,600, 500,600, 550,600, 550,1700, 500,600, 550,600, 500,600, 550,600, 
500,600, 550,1700, 500,1750, 500,1700, 500,600, 550,600, 500,600, 550,600, 550,1650, 
550,600, 500,600, 550,600, 550};

unsigned int ac_on[] = {8900,4500, 500,600, 500,600, 550,1700, 500,600, 550,1700, 
500,600, 550,600, 500,650, 500,600, 550,1700, 500,600, 550,600, 500,600, 550,1700, 500,600, 
550,600, 550,550, 550,600, 550,550, 550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,
550, 550,600, 550,600, 500,600, 550,600, 500,600, 550,600, 550,600, 500,600, 550,600, 500,600, 
550,550, 550,600, 550,600, 500,650, 500,1700, 550,1650, 550,600, 500,1700, 550,600, 500,600, 
550,600, 550,1700, 500,600, 550,600, 500,600, 550,600, 500,600, 550,1700, 500,1700, 550,1700, 
500,600, 550,600, 500,600, 550,600, 550,1650, 550,600, 500,600, 550,600, 550};

*/
unsigned int  tv_on[] = {2700,850, 450,850, 500,400, 450,400, 1350,1250, 450,400, 
500,400, 450,400, 450,450, 450,400, 500,400, 450,450, 450,400, 450,450, 450,400, 450,
450, 900,400, 450,850, 500,400, 450};

/*


void sendIR(int cod){
    switch (cod)
    {
        case 0:
            Serial.println("TV ON");
            irsend.sendRaw(tv_on, sizeof(tv_on) / sizeof(tv_on[0]), freq);
            delay(100);
            break;
        case 1:
            Serial.println("AC OFF");
            irsend.sendRaw(ac_off, sizeof(ac_off) / sizeof(ac_off[0]), freq);
            delay(100);
            break;
        /*case 3:
            Serial.println("AC ON 18c");
            irsend.sendRaw(on_18_auto_cool, sizeof(on_18_auto_cool) / sizeof(on_18_auto_cool[0]), freq);
            delay(100);
            break;
        default:
            break;
    }
}
*/

void setup(){
    // Open serial communications and wait for port to open:
    Serial.begin(57600);
    while (!Serial) continue;
    
}

void loop(){
    if(Serial.available() > 0){
        StaticJsonDocument<1500> doc;
        DeserializationError error = deserializeJson(doc, Serial);
        //JsonObject json = doc.as<JsonObject>();
        if(error){
          Serial.print(F("deserializeJson() failed: "));
          Serial.println(error.c_str());          
        } else {
          JsonArray result = doc["data"].as<JsonArray>();
          copyArray(result,code);
          
          Serial.println(sizeof(tv_on));
          
          for(i=0; i<39; i++){
            Serial.println(code[i]); 
           }
          //unsigned int* test = json["data"];
          
          Serial.println(result.size());
          Serial.println(tv_on[2]);
          //irsend.sendRaw(tv_on, sizeof(tv_on) / sizeof(tv_on[0]), freq);
          //Serial.print(test);
        }
        //Serial.println(doc);
        //command = Serial.readString();
        //Serial.println(command);
        //sendIR(command.toInt());
    }
}
