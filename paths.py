import keys
import time
import cv2 as cv
import numpy as np

#macro = bee.BeeSwarmMacro()


class PathManager:



    def __init__(self):
        self.rotation = 0

    def Hives(self):

        claimed = False
        tries = 0
        dist = 0.5

        '''keys.hold('w', 3)
        keys.hold('s', 0.5)
        keys.hold('d', 3.5)

        

        for tries in range(0, 6):

            if tries >= 1:
                dist = 1.15
            keys.hold('a', dist)

            if macro.check_screen('/home/jamal2115/vs_projects/vichop/images/claim_hive.png', 0.7):
                print("Hive found")
                claimed = True
                keys.press('e')
                break
            else:
                print("Hive not found")
                continue'''


    def Pepper(self):
        
        keys.hold('d', 5)
        keys.press('space')
        keys.hold('d', 1)
        keys.hold('w', 0.1)
        keys.hold('d', 0.1)
        keys.press('space')
        keys.hold('d', 3.5)
        keys.hold('w', 0.75)
        keys.hold('d', 0.1)
        keys.press('space')
        keys.hold('d', 1)
        keys.hold('w', 0.5)
        keys.hold('d', 0.1)
        keys.press('space')
        keys.hold('w', 3)
        keys.press('space')
        keys.hold('w', 0.5)
        keys.press('space')
        keys.hold('w', 4)
        keys.press('space')
        keys.hold('w', 4)
        keys.key_down('d')
        keys.key_down('w')
        time.sleep(3)
        keys.key_up('d')
        keys.key_up('w')
        keys.press('space')
        keys.hold('d', 5)



    def Cannon(self):
        keys.hold('d', 5)
        keys.press('space')
        time.sleep(0.1)
        keys.hold('d', 1)
        keys.hold('w', 0.1)
        keys.hold('d', 0.1)
        keys.press('space')
        for i in range(0, 2):
            keys.press('>')
            self.rotation += 45



    def Cannon_cactus(self):
        keys.press('e')
        time.sleep(2)
        keys.key_down('w')
        keys.key_down('a')
        time.sleep(1)
        keys.key_up('w')
        keys.key_up('a')

