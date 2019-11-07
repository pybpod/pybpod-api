
.. _firmware_update-label:

***************
Firmware update
***************

How to update Bpod firmware
===========================

- Download `Arduino latest version <https://www.arduino.cc/en/Main/Software>`_, extract the zip folder and save the extracted folder somewhere permanent on your PC.
- Plug the Bpod device into a USB port of the computer.
- (*Windows only*) If the drivers are not yet installed (or if you're not sure), follow Arduino Due's Windows driver installation page `here <https://www.arduino.cc/en/Guide/ArduinoDue#toc4>`_.
- Open the Arduino program folder and run Arduino.exe.
- Install support for Arduino Due (if you haven't done this already):

   * From the "Tools" menu, choose "Board" and then "Boards Manager".
   * In the boards manager, install "Arduino SAM boards (32-bits ARM Cortex M3).
   * Restart Arduino

- From the "Tools" menu, choose "Board" and then "Arduino Due (Programming Port)".
- From the "Serial Port" menu, choose "COMX" (win) or "/dev/ttySX" (linux)
  where X is the port number.To find your port number in Windows, choose "Start"
  and type "device manager" in the search window. In the device manager, scroll
  down to "Ports (COM & LPT)" and expand the menu. The COM port will be listed
  as "Arduino Due Programming Port (COMX)".

- From the File menu in Arduino, choose "Open" and select the firmware project. A new window should open with the firmware. [Download the firmware here](https://bitbucket.org/fchampalimaud/bpod-firmware)
- In the new window, click the "upload" button (the right-pointing arrow under "edit").

If all went well, the green progress indicator should finish, and be replaced
with a message: "Done uploading". Below that, in orange text, it should appear
the message "Verify successful".
