# LEDCraziness
This is an implementation of robotPy that shows how to use the AddressableLED() class. 
The gist is you instantiate the LED strand, and then every time you want to change what the strand is doing, 
you fill a dat buffer object with color, and then write that buffer to the strand. If you do this in a timed loop with a delay (like robot periodic), you can get animations.
