#include "iosetup.h"
#include <DHT.h>

const int MAX_CMD_LENGTH = 100;
const int CMD_ID_LENGTH = 3;

char serialIn[MAX_CMD_LENGTH];
int cmdParseIndex, outputVal;
String command,output;
String outputName;
int numOutputs;

DHT TM1(DHT1, DHT22);
DHT TM2(DHT2, DHT22);
DHT TM3(DHT3, DHT22);
DHT TM4(DHT4, DHT22);

float T1, T2, T3, T4;
float M1, M2, M3, M4;


void setup() {
    Serial.begin(115200);
    Serial.println("rst");

    cmdParseIndex = 0;

    pinMode(COOL_FAN, OUTPUT);
    TM1.begin();
}

void loop() {
  if(Serial.available() > 0){
    delay(20);
    int availableBytes = Serial.available();
    for(int i = 0; i < availableBytes; i++)
      serialIn[i] = Serial.read();
    
    command = readNext(';');
    if (command == "stp")  {
      Serial.println("thx;" + command);
      setOutputs();
    }
    else if (command == "log") {
      Serial.println("thx;" + command);
      logData();
    }
    else
      Serial.println("err;" + command);
  
    cmdParseIndex = 0;
    emptyInput();
  }
}

String readNext(char delim){
  bool isDone = false;
  String item = "";
  while(!isDone && cmdParseIndex < MAX_CMD_LENGTH){
    char charIn = serialIn[cmdParseIndex];
    if (charIn != delim && charIn != '\n'){
      item += (String) charIn;
      cmdParseIndex++;
    }
    else
      isDone = true; 
  }
  return item;
}

void emptyInput(){
  for(int i = 0; i < MAX_CMD_LENGTH; i++)
    serialIn[i] = NULL;
}

void setOutputs(){
  int numOutputs = readNext(';').toInt();
  for(int i = 0; i < numOutputs; i++){
    outputName = readNext(',');
    outputVal = readNext(';').toInt();
    setOutput(outputName, outputVal);
  }
}

void setOutput(String output, int outVal){
  if (output == "F1")
    digitalWrite(COOL_FAN, outVal);
  else
    Serial.println("stpErr;" + output);   
}

void logData(){
  T1 = TM1.readTemperature();
  M1 = TM1.readHumidity();


  Serial.print("dta;T1,");
  Serial.print(T1);
  Serial.print(";M1,");
  Serial.print(M1);
  Serial.println();
}
