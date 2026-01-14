import keys
import time
import cv2 as cv
import numpy as np
import buff_detection

#macro = bee.BeeSwarmMacro()




rotation = 0

def Hives():

    claimed = False
    tries = 0
    dist = 0.5

    keys.hold('w', 3)
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
            continue


def Pepper():
    
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
    keys.wait(3)
    keys.key_up('d')
    keys.key_up('w')
    keys.press('space')
    keys.hold('d', 5)
    



def Cannon():

    global rotation

    keys.hold('w', 1)
    keys.hold('d', 3)
    keys.press('space')
    keys.wait(0.1)
    keys.hold('d', 1)
    #keys.wait(0.1)
    #keys.hold('w', 0.3)
    keys.wait(0.1)
    keys.press('space')
    keys.wait(0.1)
    keys.hold('d', 0.5)




def Cannon_dandelion():
    global rotation

    time.sleep(0.5)
    keys.press('e')
    keys.wait(0.5)
    keys.press('space')
    keys.wait(0.1)
    keys.press('space')
    keys.hold('a', 1.05)
    keys.hold('w', 1.05)
    keys.press('space')
    keys.wait(3)
    
        
def Cannon_pine():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45
        
    time.sleep(0.5)
    keys.press('e')
    time.sleep(0.9)
    keys.press('space')
    time.sleep(0.1)
    keys.press('space')
    keys.key_down('w')
    keys.key_down('a')
    time.sleep(1)
    keys.key_up('w')
    keys.key_up('a')
    time.sleep(5)


def Cannon_sunflower():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    keys.wait(0.5)
    keys.press('e')
    keys.wait(0.5)
    keys.hold('d', 0.5)
    keys.press('space')
    keys.wait(3)


def Cannon_clover():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    keys.wait(0.5)
    keys.press('e')
    keys.wait(0.75)
    keys.hold('d', 1)
    keys.wait(3)
    


def Cannon_mushroom():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    time.sleep(0.5)
    keys.press('e')
    time.sleep(0.5)
    keys.press('space')
    time.sleep(0.01)
    keys.press('space')
    time.sleep(0.01)
    keys.press('space')
    time.sleep(3)
    


def Cannon_blueflower():

    global rotation

    for i in range(0, 2):
        keys.press('<')
        rotation -= 45

    time.sleep(0.65)
    keys.press('e')
    time.sleep(0.1)
    keys.hold('w', 0.16)
    time.sleep(0.08)
    keys.press('space')
    time.sleep(0.08)
    keys.press('space')
    time.sleep(0.08)
    time.sleep(4)
    keys.press('space')
    time.sleep(3)
    


def Cannon_strawberry():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    time.sleep(0.5)
    keys.press('e')
    time.sleep(0.2)
    keys.key_down('w')
    keys.press('space')
    time.sleep(0.08)
    keys.press('space')
    time.sleep(0.08)
    time.sleep(2.5)
    keys.key_up('w')
    keys.press('space')
    time.sleep(3)
    


def Cannon_spider():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    keys.wait(0.5)
    keys.press('e')
    


def Cannon_bamboo():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    keys.wait(0.5)
    keys.press('e')
    


def Cannon_pineapple():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    keys.wait(0.5)
    keys.press('e')
    


def Cannon_stump():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    keys.wait(0.5)
    keys.press('e')
    


def Cannon_pumpkin():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    keys.wait(0.5)
    keys.press('e')
    


def Cannon_cactus():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    keys.wait(0.5)
    keys.press('e')
    


def Cannon_mountain():

    global rotation

    for i in range(0, 4):
        keys.press('>')
        rotation += 45

    keys.wait(0.5)
    keys.press('e')
    