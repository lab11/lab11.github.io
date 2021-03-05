PowerBlade.
====
Low Profile True Power Meter.
-------------------

Although the information provided by large-scale plug load power metering can be
used to reduce individual power consumption, current implementations of these
plug load devices are often too large to be realistic for extremely dense
deployments. In this work, we attempt to push the limits of ultra-miniature true
power meters, and wireless sensors in general, so as to make them applicable on
a broader scale. 

PowerBlade is a single PCB that sandwiches in between the plug and the wall
outlet. There are slots on the PCB face through which the AC prongs slide before
plugging into the outlet, and flexible tabs in the slots make contact with the
prongs. This allows PowerBlade to both acquire some power and monitor the power
supplied to the AC load.

An overview of the system purpose and design can be viewed [here](https://youtu.be/oNUXhCDnHoE).

[HOMEPAGE_BREAK]

Due to the direct relationship between power supply size and output current,
miniaturization requires also reducing the power consumed in the device itself.
If the volume is reduced to an extreme (as it is in this case in order to fit
between the plug and the wall), power must also be extremely reduced as well.
PowerBlade operates on a budget of less than 1mA, and still achieves a usable
bandwidth for our application.

This extreme reduction in power available requires that the radio, the primary
consumer of power in a typical wireless sensor system, be re-thought entirely.
In PowerBlade we first successfully implemented the form factor using
backscatter communicating with an Impinj Speedway R420 reader, but this
technique requires the expense and setup of the RFID reader. Currently
PowerBlade operates using Bluetooth Low Energy (BLE), which can be read by 
commodity smartphones.


