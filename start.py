#!/bin/python
from time import sleep
from os import path
from pyautogui import click, press
from DDT_Engine import *

game = game_location()
X_GAME = game[0]
Y_GAME = game[1]
in_game = game[2] 

angle = 50
force = 50
power = '1'

# angle 55, force 45
# attack 14445678
# click 615 220 to enter
# boss cool down 15 sec

loop_count = 0
while True:
    game = check_in_game()
    in_game, chatbox_locked = game
    if chatbox_locked:
        # loby(locked)
        click(X_GAME + 670, Y_GAME + 180)
        sleep(1)
        if not loop_count <= 15:
            print('not in game for more than 15 seconds.\nprobably the game is over')
            break
        else:
            loop_count = 0
    elif not chatbox_locked and not in_game:
        # loby(unlocked)
        sleep(1)
    elif not chatbox_locked and in_game:
        # in game
        game = game_location()
        X_GAME, Y_GAME, in_game = game
        waiting_to_enter(10)
        while waiting_for_my_turn():
            print('change direction >>')
            change_angle(angle,'d')
            attack(force, power, power=True)
            sleep(5)
        for f in range(abs(15)):
            print('waiting for ', 15 - f, 'seconds', end='\r')
            sleep(1)
    sleep(1)
while True:
    game = check_in_game()
    in_game, chatbox_locked = game
    if not chatbox_locked and not in_game:
        break
        # loby(unlocked)
        # click collect function
