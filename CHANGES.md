## v.1.5.3
Bpod modules functionalities are now configured dynamically

## v.1.5.0
Update session logs format file.
Added ports enabled variable to the settings.
Fixed some bugs.

## v.1.4.0
Added compatibility with the bpod firmware v17.

## v.1.3.0 (2017/06/21)
Fixes Issue #9 - Cannot run several consecutive trials without a timer between them
Adds support for Bpod firmware version 13 (0.7.9) but keeps version 9 as default (need support from Josh)
Fixes soft codes implementation
Adds example for soft codes
Using constants for input events, input channels and output channels
Renames states for states_occurrences
Improves documentation
Simplifies the API by hiding the concept of RawData to the user and exposing only the concept of Trial

## v.1.2.0
Simplifies event collection and processing
Collect and publish live event occurrences

## v.1.1.0
Updates documentation with latest changes
Updates examples with latest changes
Includes nodejs http server for documentation
Adds documentation for event
Adds JSON plugin
Enhances trial building
Adds new example for testing states that occur several times

## v1.0.0
Use pysettings to manage this library settings
Simplifies bpod protocol by processing trial events when running state machine
Allows timeout to be defined for serial connections
Changes some logger calls
Fixes problem on bpod run where next trial could start earlier while bpod device was not ready yet (this should be fixed on the firmware instead!)
Move bpod module to a separate package
Preparing this project for GUI integration


## v.0.3.3 (2017/02/01)

Fixes a bug that would count states timestamps incorrectly
Fixes bug that would prevent correct presentation of states in the end print
Adds a new example for light chasing (2 pokes)
All examples get simplified, without using logger and with manual running hidden on a shared function
