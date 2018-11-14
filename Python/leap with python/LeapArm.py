################################################################################
# Copyright (C) 2012-2016 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time, math, cmath, serial

ArmBicep = 1000
ArmForearm = 1000
ClawBase_x = 0
ClawBase_y = 0
ClawBase_z = 0

port = 'COM3'
arduinoData = serial.Serial(port, 9600, timeout=5)
time.sleep(2)

class LeapMotionListener(Leap.Listener):



    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Motion Sensor Connected"


    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):


        # Get the most recent frame and report some basic information
        frame = controller.frame()
        #Frame object that is sent from leap motion

        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            for finger in hand.fingers:
                #Takes out index finger array
                index_finger_list = hand.fingers.finger_type(finger.TYPE_INDEX)
                index_finger = index_finger_list[0]

                #Takes out distal(final bone) from index finger
                index_finger_tip = index_finger.bone(3)

                #Prints out tip of distal and stores coordinates in each variable
                #print "Index finger tip: " + str(index_finger_tip.next_joint)
                index_x = index_finger_tip.next_joint[0]
                index_y = index_finger_tip.next_joint[1]
                index_z = index_finger_tip.next_joint[2]


                #Takes out thumb finger array
                thumb_finger_list = hand.fingers.finger_type(finger.TYPE_THUMB)
                thumb_finger = thumb_finger_list[0]

                #Takes out distal(final bone) from thumb finger
                thumb_finger_tip = thumb_finger.bone(3)
                # Prints out tip of distal and stores coordinates in each variable
                #print "Thumb finger tip: " + str(thumb_finger_tip.next_joint)
                thumb_x = thumb_finger_tip.next_joint[0]
                thumb_y = thumb_finger_tip.next_joint[1]
                thumb_z = thumb_finger_tip.next_joint[2]

        #distance time
                finger_distance = math.sqrt(math.pow(thumb_x - index_x, 2))
                #print distance

            #Finding distance to end of claw
            flat_distance = math.sqrt(math.pow(thumb_x - ClawBase_x, 2) + math.pow(thumb_z - ClawBase_z, 2))

            #3D distance to claw end
            #Uses flat distance as input variable, may be off from claw origin?
            Tip_distance = math.sqrt(math.pow(flat_distance, 2) + math.pow(thumb_y - ClawBase_y, 2))

            #acos function prints out in radians to conversion to degrees is necessary
            #Is acos the inverse function of cos?

            #Calculations within the triangle of ArmForearm, ArmBicep, and Tip_distance
            ElbowAngle = math.degrees(math.acos(  ( math.pow(ArmForearm, 2) + math.pow(ArmBicep, 2) - math.pow(Tip_distance, 2) )  /  (2 * ArmForearm * ArmBicep)  ))

            Upper_BaseAngle = math.acos(  ( math.pow(ArmBicep, 2) + math.pow(Tip_distance, 2) - math.pow(ArmForearm, 2) )  /  (2 * ArmBicep * Tip_distance)  )

            #Calculation of Lower Base angle
            Lower_BaseAngle = math.atan( (thumb_y - ClawBase_y)/ flat_distance)

            BaseAngle = math.degrees(Lower_BaseAngle + Upper_BaseAngle)

            #Calculation of Rotating Angle
            RotateAngle = math.degrees(math.atan( (thumb_x - ClawBase_x)/ (thumb_z - ClawBase_z) ))

            # Claw open/close code
            ard_FingDist = str(int(finger_distance))
            ard_ElbowA = str(int(ElbowAngle))
            ard_BaseA = str(int(BaseAngle))
            ard_RotateA = str(int(RotateAngle)+90)




            ServoAngle = [ard_FingDist, ard_ElbowA, ard_BaseA, ard_RotateA]
            ServoNames = ["ard_FingDist", "ard_ElbowA", "ard_BaseA", "ard_RotateA"]
            angleEnd = ['c', 'x', 'y', 'z']
            index = 0
            for i in ServoAngle:
                print("Python value for " + ServoNames[index] + ": ")
                i = i + angleEnd[index]

                print(i)
                arduinoData.write(i)
                time.sleep(0.05)
                index += 1

            arduinoData.flush()

            #print("Python value: ")
            #print(ard_RotateA + ";")
            #arduinoData.write(ard_RotateA + ";")
            #time.sleep(0.1)


            msg = arduinoData.read(arduinoData.inWaiting())
            print ("Message from arduino: ")
            print (msg)

            #print RotateAngle
            #print BaseAngle
            #print ElbowAngle










        """print "Frame ID: " + str(frame.id) \
            + " Timestamp: " + str(frame.timestamp) \
            + " # of Hands " + str(len(frame.hands)) \
            + " # of Fingers " + str(len(frame.fingers)) \
            + " # of Tools " + str(len(frame.tools)) \
            + " # of Gestures " + str(len(frame.gestures()))
        """




        """handType = "Left Hand" if hand.is_left else "Right Hand"

            print handType + " Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)"""

            # TYPE_MIDDLE JOINT_TIP



def main():
    # Create a sample listener and controller
    listener = LeapMotionListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    #Need to find thumb distal end and index finger distal end

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
