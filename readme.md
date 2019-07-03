## TyroS-LSL Client

This is a command-line-interface to collect data from tyroS and republish it 
via labstreaming layer. It also supports an interface to control position
and velocity of the Amadeo hand robot. (see https://tyromotion.com/)

The app is written in python 3.

# Installation


The preferred way is to clone it and install it via pip, e.g by 
```
git clone https://github.com/agricolab/app-tyros
cd app-tyros
pip install -e .
```

## Usage

You can then run it from the terminal using
```
python -m tyros.client
```
This starts a client receiving data from TyroS and pushing it via LSL.
Switching devices (re-)starts the respectice LSL outlet. Consider that the TyroS
Data Server port has to be set accordingly in the TyroS settings, and that 
TyroS only starts its data server after the calibration of the device has
been performed. 

Consider that the data interface is not natively supported by tyroS, and has
to be activated first. If in the tyroS settings, you can only see a screen
where you have to enter a key to activate the data interace, 
contact your Tyromotion sales rep, and they can help you further.

Set the interface to TCP, and the port to 61585.

Currently only the Amadeo hand robot has been implemented and tested properly.

## Amadeo

When the client detects that an Amadeo is being used, it will automatically 
request the current range of motion and append it to the LSL streaminfo. 
Consider that currently, ROM updates are therefore only performed during 
initialization.

For the Amadeo, you can also co ntrol position and velocity of each finger by 
using the respective methods of the client, e.g.
```
client.set_velocity([.1, .1, .1, .1, .1])
client.set_position([-1., -.8, -.6, -.4, -.2])
```
Please note that for the Amadeo coordinate system, -1 is maximal flexion and 
0 is maximal extension of the fingers (bound at the limits of the ROM).

Because the tyroS server only accepts one client, and we need one client
for republishing as LSL, this client has to act as a man-in-the-middle. 
This is currently not implemented.



