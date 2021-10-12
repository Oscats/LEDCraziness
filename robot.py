#!/usr/bin/env python3
"""
    This is a demo program showing the use of the RobotDrive class,
    specifically it contains the code necessary to operate a robot with
    tank drive.
"""

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID
Hand = GenericHID.Hand

from wpilib import AddressableLED
k_numberLEDs = 60


class MyRobot(wpilib.TimedRobot):
    
    #The tutorial recommends creating our own method, so I did. I created a few different methods so you can get a feel for writing animations.
    def rainbow (self):
        #Lets try to recreate the raibow effect from WPILib You can find more at the link below.
        # https://docs.wpilib.org/en/latest/docs/software/hardware-apis/misc/addressable-leds.html?highlight=addressable%20led#using-hsv-values
        #For some reason, we cannot use i as our for counter and our integer object for the count we are in.
        i = 0
        # set the first pixel hue
        rainbowFirstPixelHue= 0
        # For every pixel
        
        for d in self.dataObject:
            # Calculate the hue - hue is easier for rainbows because the color
            # shape is a circle so only one value needs to precess
            hue = (rainbowFirstPixelHue + ((i * 180 / k_numberLEDs) % 180))
            # Set the value
            self.dataObject[i].setHSV(int(hue), 255, 128)
            #increase our counter by 1
            i+=1
        # Increase our color by 3 to make the rainbow "move"
        #Note this is out of the for loop
        rainbowFirstPixelHue += 3
        # Check the Bounds and restart if it is out of bounds
        rainbowFirstPixelHue %= 180
        #light the lights (You could move this to create a chase scene)
        self.led.setData(self.dataObject)
    def chase (self):
        
        #Now, let's try a wipe sequence...
        wipePixel = 0
        # set the first pixel hue
        color1=(255,0,255)
        # For every pixel
        #data = [AddressableLED.LEDData(0, 0, 0) for _ in range(k_numberLEDs)]
        color2 = (0,255,0)
        if ((self.colorPosition < (k_numberLEDs)) and (self.colorFlag == False)):
            # Calculate the hue - hue is easier for rainbows because the color
            # shape is a circle so only one value needs to precess
            #hue = (rainbowFirstPixelHue + ((i * 180 / k_numberLEDs) % 180))
            # Set the value
            self.dataObject[self.colorPosition].setRGB(color1[0], color1[1], color1[2])
            #increase our counter by 1
            self.colorPosition+=1 
        elif ((self.colorPosition< k_numberLEDs) and (self.colorFlag == True)):
             # Calculate the hue - hue is easier for rainbows because the color
            # shape is a circle so only one value needs to precess
            #hue = (rainbowFirstPixelHue + ((i * 180 / k_numberLEDs) % 180))
            # Set the value
            self.dataObject[self.colorPosition].setRGB(color2[0], color2[1], color2[2])
            #increase our counter by 1
            self.colorPosition+=1 
        else:
            self.colorPosition=0
            self.colorFlag = not self.colorFlag
        self.led.setData(self.dataObject)

    def singleLed (self):
        
        #Now, let's try light just one light...
        #first, we set the object's color
        self.dataObject[30].setRGB(255, 0, 100)
        #Then, we write the buffer to the strip.           
        self.led.setData(self.dataObject)

    def robotInit(self):
        """Robot initialization function"""

        # object that handles basic drive operations
        self.frontLeftMotor = wpilib.Talon(0)
        self.rearLeftMotor = wpilib.Talon(1)
        self.frontRightMotor = wpilib.Talon(2)
        self.rearRightMotor = wpilib.Talon(3)

        self.left = wpilib.SpeedControllerGroup(self.frontLeftMotor, self.rearLeftMotor)
        self.right = wpilib.SpeedControllerGroup(
            self.frontRightMotor, self.rearRightMotor
        )

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        # joysticks 1 & 2 on the driver station
        self.stick = wpilib.XboxController(0)
        #self.led_screen_led = wpilib.AddressableLED(5)
        #Instantiate an LED Object on PWM pin 5.
        self.led = AddressableLED(5)
        #set the number of leds
        self.led.setLength(k_numberLEDs)

        #Create an LED Data Object for the color
        self.data = AddressableLED.LEDData(255, 0, 0) # I could not get this to instantiate without passing a color.
        
        # Write the buffer to the strip
        self.led.setData([self.data]*k_numberLEDs)
        #start the strip lighting (You only need to do this once.)
        self.led.start()
        self.colorFlag = False
        self.colorPosition = 0

        #Create another data object for custom animations (this may be redundant, but I got errors when I attempted to use the same one.)
        self.dataObject = [AddressableLED.LEDData(0, 0, 0) for _ in range(k_numberLEDs)]

    def teleopInit(self):
        """Executed at the start of teleop mode"""
        self.myRobot.setSafetyEnabled(True)
        # Call the method to light the lights in a rainbow
        self.rainbow()
        
    def teleopPeriodic(self):
        """Runs the motors with tank steering"""
        self.myRobot.tankDrive(self.stick.getRawAxis(4) * -1, self.stick.getRawAxis(1) * -1)
        self.stick.setRumble(GenericHID.RumbleType.kRightRumble,1)
        #self.chase()
        self.singleLed()

    def disabledInit(self):
        # Do not forget to disable the rumbling in robot disabled mode
        self.stick.setRumble(GenericHID.RumbleType.kRightRumble,0)
        #Turn the strip back to the color you choose.
        #It would be cool if this were the color of our alliance.
        self.led.setData([self.data]*k_numberLEDs)


if __name__ == "__main__":
    wpilib.run(MyRobot)