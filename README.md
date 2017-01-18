# pybpod-api

## About
TODO

## Developers Team

The [Scientific Software Platform (SWP)](http://research.fchampalimaud.org/en/research/platforms/staff/Scientific%20Software/) from the Champalimaud Foundation provides technical know-how in software engineering and high quality software support for the Neuroscience and Cancer research community at the Champalimaud Foundation.

We typical work on computer vision / tracking, behavioral experiments, image registration and database management.

* [@cajomferro](https://github.com/cajomferro/) Carlos Mão de Ferro
* [@JBauto](https://github.com/JBauto) João Baúto
* [@UmSenhorQualquer](https://github.com/UmSenhorQualquer/) Ricardo Ribeiro

## Bpod project
**pybpod-api** is a python port of the [Bpod Matlab project](https://github.com/sanworks/Bpod). 

All examples and Bpod's state machine and communication logic were based on the original version made available by [Josh Sanders](https://github.com/sanworks).

## License
This is Open Source software. We use the MIT license, which provides almost no restrictions on the use of the code.

## Running examples

1. Duplicate *user_settings.py.template* and save it as *user_settings.py*

        Define the SERIAL_PORT attribute with your machine serial port where Bpod is connected to
        Define the API_LOG_LEVEL with logging.DEBUG if you want detailed logging for the API

2. On the project root folder run:
    
        pip3 install -r requirements.txt --upgrade # installs dependencies
        pip3 install . # installs this API
    
3. Then move to the examples folder and run example:
 
        cd PROJECT_FOLDER/examples/function_examples
        python3 add_trial_events.py # run example
