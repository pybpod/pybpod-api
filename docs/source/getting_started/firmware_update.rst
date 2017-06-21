
.. _firmware_update-label:

***************
Firmware update
***************

How to update Bpod firmware
===========================

1. Download `Arduino latest version <https://www.arduino.cc/en/Main/Software>`_, extract the zip folder and save the extracted folder somewhere permanent on your PC.
2. Plug the Bpod device into the governing computer's USB port.
3. (*Windows only*) If the drivers are not yet installed (or if you're not sure), follow Arduino Due's Windows driver installation page.
4. Open the Arduino program folder and run Arduino.exe.
5. Install support for Arduino Due (if you haven't done this already):

   * From the "Tools" menu, choose "Board" and then "Boards Manager".
   * In the boards manager, install "Arduino SAM boards (32-bits ARM Cortex M3).
   * Restart Arduino

6. From the "Tools" menu, choose "Board" and then "Arduino Due (Programming Port)".
7. From the "Serial Port" menu, choose "COMX" (win) or "/dev/ttySX" (linux) where X is the port number. To find your port number in Win7, choose "Start" and type "device manager" in the search window. In the device manager, scroll down to "Ports (COM & LPT)" and expand the menu. The COM port will be listed as "Arduino Due Programming Port (COMX)".
8. From the File menu in Arduino, choose "Open" and select "C:\Bpod\Bpod Firmware\Bpod0_X\Bpod_MainModule_0_X_Y\Bpod_MainModule_0_X_Y.ino. A new window should open with the firmware.
9. In the new window, click the "upload" button (the right-pointing arrow under "edit").

If all went well, the green progress indicator should finish, and be replaced with a message: "Done uploading". In orange text below, should read "Verify successful".
