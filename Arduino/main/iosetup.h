/* iosetup.h 
 * Setup for inuputs and outputs in greenhouse
 * Started 2020-06-05
 * Created by Leif Blake
 */

#ifndef IOSETUP_H
#define IOSETUP_H

//RS485 Shield
//Shield should be in ON/MANU setting
#define RS485_EN 2 //Using pins 0 and 1 for Rx and Tx
#define SOIL1_ADDR 1 //For ST1 and SM1
#define SOIL2_ADDR 4 //For ST2 and SM2

//Motor Controller Shield
#define MOTOR_DIR 12
#define MOTOR_PWM 3

//DHT22 Sensors (Air Temp and Humidity)
#define DHT1 4 //For T1 and M1
#define DHT2 5 //For T2 and M2
#define DHT3 6 //For T3 and M3
#define DHT4 7 //For T4 and M4

//Digital inputs
#define WATER_TEMP A1 //Reservoir water temperature
#define WATER_HIGH A2 //float switch near top of reservoir
#define WATER_LOW A3 //float switch near bottom of reservoir
#define WINDOW1 A4 //detects if window is open
#define DOOR A5 // detects if door is open
#define LIMIT1 SDA
#define LIMIT2 SCL

//Outputs
#define COOL_FAN 8 //air intake from the north wall
#define BLOWER 9 //circulating air
#define VALVE1 10 //water to zone 1
#define VALVE2 11 //water to zone 2
#define VALVE_IN 13 //filling up the water tank

#endif
