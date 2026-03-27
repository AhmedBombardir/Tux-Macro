from keys import *
import time
import cv2 as cv
import numpy as np
import buff_detection
import subprocess
import settings

#macro = bee.BeeSwarmMacro()


rotation = 0

def Hives():

    claimed = False
    tries = 0
    dist = 0.5

    hold('w', 3)
    hold('s', 0.5)
    hold('d', 3.5)

    

    for tries in range(0, 6):

        if tries >= 1:
            dist = 1.15
        hold('a', dist)

        if macro.check_screen('/home/jamal2115/vs_projects/vichop/images/claim_hive.png', 0.7):
            print("Hive found")
            claimed = True
            press('e')
            break
        else:
            print("Hive not found")
            continue


def Pepper():
    
    hold('d', 5)
    press('space')
    hold('d', 1)
    hold('w', 0.1)
    hold('d', 0.1)
    press('space')
    hold('d', 3.5)
    hold('w', 0.75)
    hold('d', 0.1)
    press('space')
    hold('d', 1)
    hold('w', 0.5)
    hold('d', 0.1)
    press('space')
    hold('w', 3)
    press('space')
    hold('w', 0.5)
    press('space')
    hold('w', 4)
    press('space')
    hold('w', 4)
    key_down('d')
    key_down('w')
    wait(3)
    key_up('d')
    key_up('w')
    press('space')
    hold('d', 5)
    
    

def Reset():
    global rotation

    time.sleep(1)
    press('esc')
    time.sleep(1)
    press('r')
    time.sleep(0.25)
    press('enter')
    time.sleep(3)
    
    
    press('o')

    for i in range(6):
        press('o')
        time.sleep(0.01)
    time.sleep(3) 

    rotation = 0
 

def Reset_p2():

    for i in range(6):
        press('o')
        time.sleep(0.01)
    time.sleep(3)


def Cannon():

    global rotation
    rotation = 0


    time.sleep(0.5)
    hold('w', 1)
    hold('s', 0.1)
    hold('d', 1 * settings.hiveSlot)
    press('space')
    time.sleep(0.15)
    key_down('d')
    key_down('w')
    time.sleep(0.25)
    key_up('d')
    key_up('w')
    #wait(0.1)
    #hold('w', 0.3)
    hold('d', 1)

    






def Cannon_dandelion():
    global rotation

    time.sleep(0.5)
    press('e')
    time.sleep(0.5)
    press('space')
    time.sleep(0.1)
    press('space')
    hold('a', 1.25)
    hold('w', 1)
    press('space')
    time.sleep(3)
    
        
def Cannon_pine():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45
        
    time.sleep(0.5)
    press('e')
    time.sleep(0.9)
    press('space')
    time.sleep(0.1)
    press('space')
    key_down('w')
    key_down('a')
    time.sleep(1)
    key_up('w')
    key_up('a')
    time.sleep(6)
    hold('s', 0.1)
    hold('d', 0.1)
    time.sleep(1)


def Cannon_sunflower():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    time.sleep(0.5)
    press('e')
    time.sleep(0.35)
    press('space')
    time.sleep(0.08)
    press('space')
    hold('a', 1.1)
    press('space')
    time.sleep(3)


def Cannon_clover():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    time.sleep(0.5)
    press('e')
    time.sleep(1)
    press('space')
    time.sleep(0.08)
    press('space')
    key_down('s')
    key_down('d')
    time.sleep(3)
    key_up('s')
    key_up('d')
    press('space')
    time.sleep(5)
    


def Cannon_mushroom():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    time.sleep(0.5)
    press('e')
    time.sleep(0.5)
    press('space')
    time.sleep(0.01)
    press('space')
    time.sleep(0.01)
    press('space')
    time.sleep(3)
    


def Cannon_blueflower():

    global rotation

    for i in range(0, 2):
        press('<')
        rotation -= 45

    time.sleep(0.65)
    press('e')
    time.sleep(0.1)
    hold('w', 0.16)
    time.sleep(0.08)
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(0.08)
    time.sleep(4)
    press('space')
    time.sleep(3)
    


def Cannon_strawberry():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    time.sleep(0.5)
    press('e')
    time.sleep(0.5)
    key_down('w')
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(0.08)
    hold('a', 0.9)
    time.sleep(1.25)
    key_up('w')
    press('space')
    time.sleep(3)
    


def Cannon_spider():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    time.sleep(0.5)
    press('e')

    time.sleep(1.5)
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(0.5)
    press('space')
    


def Cannon_bamboo():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    time.sleep(0.5)
    press('e')
    time.sleep(0.01)
    hold('d', 0.4)
    time.sleep(0.7)
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(2)
    press('space')
    time.sleep(3)

    
def Cannon_rose():
    
    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    time.sleep(0.5)
    press('e')
    time.sleep(0.05)
    hold('a', 0.4)
    press('space')
    time.sleep(0.1)
    press('space')
    time.sleep(3)
    press('space')
    time.sleep(3)

def Cannon_pineapple():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    wait(0.5)
    press('e')
    time.sleep(1.75)
    key_down('d')
    press('space')
    time.sleep(0.08)
    press('space')
    key_up('d')
    time.sleep(3.2)
    press('space')
    time.sleep(3)
    


def Cannon_stump():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    wait(0.5)
    press('e')
    time.sleep(1.75)
    key_down('d')
    press('space')
    time.sleep(0.08)
    press('space')
    key_up('d')
    time.sleep(2.5)
    hold('d', 2.5)
    time.sleep(3)
    


def Cannon_pumpkin():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    time.sleep(0.5)
    press('e')

    key_down('w')
    key_down('a')
    time.sleep(1.1150)
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(3.25)
    key_up('w')
    key_up('a')
    press('space')
    time.sleep(4)
    


def Cannon_cactus():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    wait(0.5)
    press('e')

    key_down('w')
    key_down('a')
    time.sleep(0.9)
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(2.5)
    key_up('w')
    key_up('a')
    press('space')
    time.sleep(4)


def Cannon_mountain():

    global rotation

    for i in range(0, 4):
        press('>')
        rotation += 45

    wait(0.5)
    press('e')
    time.sleep(4)


def Cannon_wealth_clock():

    global rotation
    
    for i in range(0, 2):
        press('<')
        rotation -= 45

    time.sleep(0.5)
    press('e')
    hold('w', 0.5)
    press('space')
    time.sleep(0.08)
    press('space')
    key_down('w')
    key_down('d')
    time.sleep(1)
    key_up('w')
    key_up('d')
    hold('w', 0.5)
    time.sleep(3)
    hold('w', 3)
    hold('d', 0.2)
    press('space')
    time.sleep(0.08)
    hold('w', 2)
    press('e')
    time.sleep(1)


def Cannon_mondo():

    global rotation

    time.sleep(0.5)
    press('e')
    time.sleep(3)
    hold('d', 2)
    time.sleep(30)


def Ant_pass():

    global rotation

    time.sleep(0.5)
    press('e')
    time.sleep(1.5)
    press('space')
    time.sleep(0.08)
    press('space')
    key_down('w')
    key_down('a')
    time.sleep(1)
    key_up('w')
    key_up('a')
    hold('w', 0.5)
    time.sleep(5)
    hold('w', 6.25)
    key_down('s')
    key_down('a')
    time.sleep(4)
    key_up('s')
    key_up('a')
    key_down('w')
    key_down('d')
    time.sleep(1)
    key_up('w')
    key_up('d')
    hold('s', 1.25)
    hold('w', 0.5)
    time.sleep(0.5)
    press('e')
    time.sleep(1)


def Cannon_robo_pass():

    global rotation
    
    for i in range(0, 4):
        press('<')
        rotation += 45

    time.sleep(0.5)
    press('e')

    time.sleep(3)
    hold('w', 5)
    hold('a', 5)
    hold('d', 1)
    hold('w', 1.9)

    for i in range(0,2):
        press('<')
        rotation += 45
    
    hold('w', 1)
    time.sleep(0.08)
    press('space')
    time.sleep(0.5)
    hold('w', 1)
    hold('a', 0.5)
    hold('w', 3)
    time.sleep(0.5)
    press('e')
    time.sleep(1)


def Honey_dispenser():

    global rotation

    time.sleep(0.5)
    press('e')

    time.sleep(0.451)
    press('space')
    time.sleep(0.08)
    press('space')
    key_down('w')
    key_down('a')
    time.sleep(3.255)
    key_up('w')
    key_up('a')
    press('space')
    time.sleep(2)
    press('e')
    time.sleep(1)



def Treat_dispenser():

    global rotation
    
    for i in range(0,4):
        press('<')

    time.sleep(0.5)
    press('e')
    time.sleep(0.7)
    press('space')
    time.sleep(0.08)
    press('space')
    
    hold('d', 2)
    hold('w', 3)
    press('space')
    time.sleep(3)
    

def Cannon_blueberry_dispenser():

    global rotation

    time.sleep(0.5)
    press('e')


def Cannon_strawberry_dispenser():

    global rotation

    time.sleep(0.5)
    press('e')



def Coconut_dispenser():

    global rotation

    time.sleep(0.5)
    press('e')


def Glue_dispenser():

    global rotation

    time.sleep(0.5)
    press('e')


def Cannon_stockings():

    global rotation

    time.sleep(0.5)
    press('e')
    
    time.sleep(1.1)
    press('space')
    time.sleep(0.08)
    press('space')
    key_down('w')
    key_down('a')
    time.sleep(5)
    key_up('w')
    key_up('a')
    press('space')
    time.sleep(2.5)
    press('e')
    time.sleep(1)
    hold('w', 0.5)
    hold('s', 0.5)
    hold('a', 1)
    hold('d', 2)
    time.sleep(3)

def wreath():

    global rotation

    time.sleep(0.5)

    hold('d', 3)
    hold('a', 0.75)
    press('e')
    time.sleep(3)

def Cannon_feast():

    global rotation

    for i in range(0, 4):
        press('<')

    time.sleep(0.5)
    press('e')
    
    hold('w', 0.3)
    time.sleep(0.5)
    
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(1)
    key_down('w')
    key_down('a')
    time.sleep(0.75)
    key_up('w')
    key_up('a')
    hold('w', 0.525)
    press('space')

    time.sleep(2)
    press('e')
    time.sleep(1.5)
    hold('d', 0.25)
    hold('w', 0.5)
    hold('a', 0.25)
    hold('s', 0.5)
    hold('a', 0.25)
    hold('w', 0.25)


def Cannon_robo_party():

    global rotation

    time.sleep(0.5)
    press('e')
    
    time.sleep(0.75)
    key_down('d')
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(4.4)
    key_up('d')
    hold('w', 0.7)
    press('space')
    time.sleep(2)
    press('e')
    time.sleep(1)
    

def Cannon_gingerbread():

    global rotation

    for i in range(0,4):
        press('<')
        rotation += 0.45


    time.sleep(0.5)
    press('e')
    
    time.sleep(0.35)


    key_down('w')
    key_down('a')

    press('space')
    time.sleep(0.08)
    press('space')

    time.sleep(0.95)
    key_up('w')
    key_up('a')
    
    press('space')
    time.sleep(2)

    hold('w', 1.1)
    
    time.sleep(0.75)

    press('e')
    time.sleep(3)



def Cannon_snow_machine():

    global rotation
    
    for i in range(0, 4):
        press('<')

    time.sleep(0.5)
    press('e')
    
    time.sleep(1)
    key_down('d')
    key_down('s')
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(2)
    key_up('s')
    key_up('d')
    key_down('d')
    time.sleep(4)
    key_up('d')
    hold('w', 0.5)
    hold('a', 2.5)
    hold('d', 0.25)
    time.sleep(0.5)
    press('e')
    time.sleep(3)

def Cannon_candles():

    global rotation

    time.sleep(0.5)
    press('e')
    
    time.sleep(0.5)
    key_down('d')
    key_down('w')
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(2.8)
    key_up('w')
    time.sleep(3)
    key_up('d')
    hold('a', 0.25)
    press('e')
    time.sleep(2)
    hold('d', 0.75)
    time.sleep(0.5)


def Cannon_honeystorm():

    global rotation

    time.sleep(0.5)
    press('e')
    
    time.sleep(1.5)
    key_down('w')
    key_down('a')
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(4.25)
    key_up('a')
    time.sleep(0.5)
    key_up('w')
    press('space')
    time.sleep(2)
    press('e')
    time.sleep(1)

def Cannon_samovar():

    global rotation

    for i in range(0,4):
        press('<')
        rotation -= 45

    time.sleep(0.5)
    press('e')

    time.sleep(2)
    key_down('d')
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(10)
    key_up('d')
    key_down('w')
    key_down('a')
    time.sleep(7)
    key_up('w')
    key_up('a')
    press('space')
    time.sleep(0.08)
    key_down('w')
    key_down('d')
    time.sleep(3)
    key_up('w')
    key_up('d')
    press('space')
    time.sleep(0.08)
    key_down('w')
    key_down('d')
    time.sleep(1.5)
    key_up('w')
    key_up('d')
    press('space')
    time.sleep(0.08)
    key_down('d')
    key_down('w')
    time.sleep(3)
    key_up('w')
    key_up('d')
    hold('s', 0.25)
    hold('a', 0.25)
    time.sleep(1)

def Cannon_lid_art():

    global rotation

    for i in range(0, 4):
        press('<')
        rotation -= 45

    time.sleep(0.5)
    press('e')
    
    time.sleep(3)
    hold('w', 4)
    hold('a', 4)
    hold('d', 0.6)
    hold('w', 6)
    press('space')
    time.sleep(0.08)
    hold('w', 5)
    press('space')
    time.sleep(0.08)
    hold('w', 0.4)
    time.sleep(3)

def Cannon_gummy_beacon():

    global rotation
    
    time.sleep(0.5)
    press('e')

    time.sleep(0.7)
    key_down('w')
    key_down('a')
    press('space')
    time.sleep(0.08)
    press('space')
    time.sleep(3)
    key_up('w')
    key_up('a')

