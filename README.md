# pybpod-api

## About
### What is Bpod?

**Bpod** is a system from [Sanworks](<https://sanworks.io/index.php>) for precise measurement of small animal behavior.
It is a family of open source hardware devices which includes also software and firmware to control these devices.

**Bpod** software was originally developed in Matlab providing retro-compatibility with the [BControl](<http://brodywiki.princeton.edu/bcontrol/index.php/Main_Page>`) system.

### What is pybpod-api?
Python is one of the most popular programming languages today [[1]](https://pypl.github.io/PYPL.html). This is special true for the science research community because it is an open language, easy to learn, with a strong support community and with a lot of libraries available.

**pybpod-api** is a Python library that enables communication with the latest [Bpod device](https://sanworks.io/shop/viewproduct?productID=1011) version.

You can use it directly as a CLI (Command Line Interface) or use your favorite GUI to interact with it.


## Developers Team

The [Scientific Software Platform (SWP)](http://research.fchampalimaud.org/en/research/platforms/staff/Scientific%20Software/) from the Champalimaud Foundation provides technical know-how in software engineering and high quality software support for the Neuroscience and Cancer research community at the Champalimaud Foundation.

We typical work on computer vision / tracking, behavioral experiments, image registration and database management.

* [@cajomferro](https://github.com/cajomferro/) Carlos Mão de Ferro
* [@JBauto](https://github.com/JBauto) João Baúto
* [@UmSenhorQualquer](https://github.com/UmSenhorQualquer/) Ricardo Ribeiro
* [@MicBoucinha](https://github.com/MicBoucinha/) Luís Teixeira

## Bpod project
**pybpod-api** is a python port of the [Bpod Matlab project](https://github.com/sanworks/Bpod). 

All examples and Bpod's state machine and communication logic were based on the original version made available by [Josh Sanders](https://github.com/sanworks).

## License
This is Open Source software with an MIT license.

## Running examples

1. Duplicate *user_settings.py.template* and save it as *user_settings.py*

        Define the PYBPOD_SERIAL_PORT attribute with your machine serial port where Bpod is connected to
        Define the API_LOG_LEVEL with logging.DEBUG if you want detailed logging for the API

2. On the project root folder run:
    
        pip3 install -r requirements.txt --upgrade # installs dependencies
        pip3 install . # installs this API
    
3. Then move to the examples folder and run example:
 
        cd PROJECT_FOLDER/examples/function_examples
        python3 add_trial_events.py # run example
