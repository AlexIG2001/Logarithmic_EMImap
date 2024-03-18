# EMI mapping with AD8307 and OpenCV




Software dependencies for the python scripts:
* OpenCV (`sudo apt install python3-opencv && pip3 install opencv-contrib-python imutils setuptools`)
* Pyserial (`pip3 instal pyserial`)
* pyrtlsdr (`sudo apt install rtl-sdr && pip3 install pyrtlsdr`)
* numpy, scipy, matplotlib (`pip3 install scipy numpy matplotlib`)




## Method #2: Camera EMI mapping

To make an EM map with the machine vision method:
1. Launch the script (optionnal arguments, refer to the help),
2. Properly position the device under test (DUT) in the camera image,
3. Press "R" to set the position (**the camera and DUT must not move after pressing "R"**),
4. Put the probe in the frame, press "S", select the probe with the mouse and press "ENTER" to start the scanning,
5. Scan the DUT by moving the probe,
6. Press "Q" to exit. If a scan was made, the result is displayed.

