#!/bin/python
from os import path, remove
from time import sleep, time
from pyautogui import locateOnScreen as LOS, locate
from pyautogui import keyDown, keyUp, press, screenshot, write
from pyautogui import ImageNotFoundException

images_dir = 'Images'
global X_GAME
global Y_GAME

def game_location():
    global X_GAME, Y_GAME
    loop_count=0
    while True:
        loop_count=loop_count+1
        print('searching for the game location (' + str(loop_count) + ' times)', end='\r')
        if path.exists('screenshot.png') is True:
            remove('screenshot.png')
        sleep(0.1)
        screenshot('screenshot.png')
        try:
            location = locate(path.join(images_dir, 'LockChat.png'),
                              'screenshot.png', grayscale=True, confidence=0.9)
            print('\nfound in loby chat box (locked)')
            in_game = False
            X_GAME = location[0] - 16     # calibrated
            Y_GAME = location[1] - 453    # calibrated
            break
        except ImageNotFoundException:
            pass
        try:
            location = locate(path.join(images_dir, 'LockChat2.png'),
                              'screenshot.png', grayscale=True, confidence=0.9)
            print('\nfound in loby chat box (unlocked)')
            in_game = False
            X_GAME = location[0] - 16    # calibrated
            Y_GAME = location[1] - 452   # calibrated
            break
        except ImageNotFoundException:
            pass
        try:
            location = locate(path.join(images_dir, 'LockChat-InGame.png'),
                              'screenshot.png', grayscale=True, confidence=0.9)
            print('\nfound in game chat box')
            in_game = True
            X_GAME = location[0] - 7     # calibrated
            Y_GAME = location[1] - 162   # calibrated
            break
        except ImageNotFoundException:
            pass

        sleep(1)
    print("Game Coordinates :", str(X_GAME) + 'x' + str(Y_GAME), 'with radius of 1000x600')
    return[X_GAME, Y_GAME, in_game]

def waiting_to_enter(delay):
    global X_GAME, Y_GAME
    print('waiting to enter the game')
    loop_count=0
    loop_started=False
    while True:
        try:
            LOS(path.join(images_dir, 'GearLogo.png'), grayscale=True, region=(X_GAME + 940, Y_GAME, 35, 25), confidence=0.8)
            if loop_started:
                print('\n')
            print('entering the room')
            print('sleeping for', delay, 'seconds to avoid animation')
            for f in range(abs(delay)):
                print('sleep (' + str(f + 1) + '/' + str(delay) + ')', end='\r')
                sleep(1)
            break
        except ImageNotFoundException:
            loop_count=loop_count+1
            print('still waiting... (' + str(loop_count) + ' times)' , end='\r')
        sleep(1)
    return

def waiting_for_my_turn():
    global X_GAME, Y_GAME
    waiting_time=0
    loop_started=False
    while True:
        try:
            LOS(path.join(images_dir, 'Plus2.png'), grayscale=True,
                         region=(X_GAME + 950, Y_GAME + 115, 45, 55), confidence=0.8)
            if loop_started:
                print('\nits my turn')
            else:
                print('its my turn')
            break
        except ImageNotFoundException:
            loop_started=True
            waiting_time = waiting_time + 1
            print('its not my turn (' + str(waiting_time) + '/5)', end='\r')
            if waiting_time == 5:
                print('\nin game check : ', end='')
                loop_started=False
                try:
                    LOS(path.join(images_dir, 'GearLogo.png'), grayscale=True,
                                  region=(X_GAME + 940, Y_GAME, 35, 25))
                    print('True')
                    sleep(0.5)
                    waiting_time = 0
                except ImageNotFoundException:
                    print('False')
                    return False
        sleep(0.5)
    return True

def get_angle(angle=None):
    debug = True
    global X_GAME, Y_GAME
    if path.exists('screenshot.png') is True:
        remove('screenshot.png')
    sleep(0.1)
    screenshot('screenshot.png', region=(int(X_GAME) , int(Y_GAME) , 1000, 600))
    if angle is None:
        angle_1 = 0
        angle_2 = 0
        for f in range(0, 10):
            try:
                if debug:
                    print('scanning angle :', f * 10, end='\r' )
                locate(path.join(images_dir, str(f) + '.png'), 'screenshot.png',
                                 region=(33, 556, 21, 21), grayscale=True, confidence=0.8)
                angle_1 = f * 10
                break
            except ImageNotFoundException:
                pass

        for g in range(0, 10):
            try:
                if debug:
                    print('scanning angle :', angle_1 + g, end='\r')
                locate(path.join(images_dir, str(g) + '.png'), 'screenshot.png',
                       region=(46, 556, 21, 21), grayscale=True, confidence=0.8)
                angle_2 = g
                break
            except ImageNotFoundException:
                pass
        print('')
        if (angle_1 is not None) and (angle_2 is not None):
            return angle_1 + angle_2
        else:
            return None
    elif angle is not None:
        angle = str(angle)
        if debug:
            print('test if angle is :', angle)
        try:
            locate(path.join(images_dir, str(angle[0]) + '.png'), 'screenshot.png',
                   region=(33, 556, 21, 21), grayscale=True, confidence=0.8)

            locate(path.join(images_dir, str(angle[1]) + '.png'), 'screenshot.png',
                   region=(46, 556, 21, 21), grayscale=True, confidence=0.8)
            return True
        except ImageNotFoundException:
            return False


def change_angle(wanted_angle, RLDirection=''):
    global X_GAME, Y_GAME
    press(RLDirection)
    current_angle = get_angle()
    if current_angle is None:
        print('cant detect angle.')
        return False
    print('current angle is :', current_angle )
    loop_count=0
    while True:
        if (current_angle is not None) and (current_angle != wanted_angle):
            if current_angle < wanted_angle:
                press('w', presses=(wanted_angle - current_angle))
            elif current_angle > wanted_angle:
                press('s', presses=(current_angle - wanted_angle))
        # if the current angle is either more than 99 or lower than 0 
        if current_angle is None:
            press('w', presses=5)

        # if current angle is still not wanted angle even after we changes the angle above
        test_angle = get_angle(wanted_angle)
        if test_angle:
            break
        elif (current_angle is not None) and (current_angle != wanted_angle):
            keyDown(RLDirection)
            sleep(0.005)
            keyUp(RLDirection)
        current_angle = get_angle()
        #if loop_count <= 15:
        #    loop_count=loop_count+1
        #else:
        #    print('loop for more than 15 times. returning')
        #    return False
    return True

def attack(force,key,power=False):
    global X_GAME, Y_GAME
    calibrate = 4
    force_calibrate = force - calibrate

    sleep(0.2)
    if power:
        try:
            LOS(path.join(images_dir, 'pow.png'), grayscale=True,
                              region=(X_GAME + 920, Y_GAME + 515, 65, 60), confidence=0.8)
            print('normal attack at force', force, '(calibrate to', force_calibrate,')' )
        except ImageNotFoundException:
            print('power attack at force', force, '(calibrate to', force_calibrate,')' )
            press('b')
    elif not power:
        print('normal attack at force', force, '(calibrate to', force_calibrate,')' )
    write(key)
    sleep(0.2)
    keyDown('space')
    for f in (range(abs(force_calibrate))):
        sleep(0.04)
        print('force : ',f + calibrate + 1,end='\r')
    print('\nsending key : 4445678')
    write('4445678')
    keyUp('space')
    sleep(3)
    return

def waiting_for_loby():
    print('waiting to get back to loby', end='\r')
    loop_count=0
    start_time=time()
    while True:
        loop_count=loop_count+1
        print('waiting to get back to lopy (' + str(loop_count) + ' times)' ,end='\r')
        try:
            LOS(path.join(images_dir, 'LockChat2.png'), grayscale=True,
                region=(X_GAME + 4, Y_GAME + 442, 35, 35), confidence=0.9)
            print('\non loby, waited for', int(time() - start_time), 'seconds')
            break
        except ImageNotFoundException:
            sleep(1)
    return

def check_in_game():
    global X_GAME, Y_GAME
    while True:
        print('check if in game : ', end='')
        if path.exists('screenshot.png') is True:
            remove('screenshot.png')
        sleep(0.1)
        screenshot('screenshot.png', region=(int(X_GAME) , int(Y_GAME) , 1000, 600))
        try:
            location = locate(path.join(images_dir, 'LockChat.png'),
                              'screenshot.png', grayscale=True, confidence=0.9)
            print('loby(locked)')
            in_game = False
            chatbox_locked = True
            break
        except ImageNotFoundException:
            pass
        try:
            location = locate(path.join(images_dir, 'LockChat2.png'),
                              'screenshot.png', grayscale=True, confidence=0.9)
            print('loby(unlocked)')
            in_game = False
            chatbox_locked = False
            break
        except ImageNotFoundException:
            pass
        try:
            location = locate(path.join(images_dir, 'LockChat-InGame.png'),
                              'screenshot.png', grayscale=True, confidence=0.9)
            print('in game')
            in_game = True
            chatbox_locked = False
            break
        except ImageNotFoundException:
            pass
        print('unknoun')
        sleep(0.5)
    return (in_game, chatbox_locked)

