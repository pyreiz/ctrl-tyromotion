## TyroS-LSL Client

This is a command-line-interface to collect data from a tyroS and stream it via labstreaming layer. 

The app is written in python 3.

# Installation


The preferred way is to clone it and install it via pip, e.g by 
```
git clone https://github.com/agricolab/app-tyros
cd app-tyros
pip install -e .
```

## Usage

```
python -m tyros.client
```

Running this from the terminal starts a client receiving data from TyroS and 
pushing it via LSL. Switching devices (re-)starts the respectice LSL outlet. 
Consider that the TyroS Data Server port has to be set accordingly in the TyroS
settings, and that TyroS only starts its data server after the calibration 
of the device has been performed. 

Additionally, currently only the Amadeo hand robot has been tested.


