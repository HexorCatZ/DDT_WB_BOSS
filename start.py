#!/bin/python
from os import chdir, getcwd, path, remove
from datetime import datetime, timedelta
from time import sleep
from pyautogui import center, click, keyDown, keyUp, locate, locateAllOnScreen, locateOnScreen, press, screenshot, typewrite
from pyautogui import locateOnScreen

# all setting location is here
working_dir = "/tmp"
images_dir = "Images"
python_dir = getcwd()

# avoiding filepath error after changing a directory
if path.exists('Images') is True:
	images_dir = python_dir + '/' + images_dir
if path.exists(working_dir) is True:
	chdir(working_dir)
else:
	print(path.basename(__file__), ':', working_dir, ':', 'file not found')
	exit(1)

print("searching for the game location")
game_location = locateOnScreen(images_dir + '/' + 'LockChat.png', confidence=0.9)
while game_location is None:
	sleep(1)
	game_location = locateOnScreen(images_dir + '/' + 'LockChat.png', confidence=0.9)

X_GAME = game_location[0] - 16
Y_GAME = game_location[1] - 453
GAME_HEIGHT = 599
GAME_WIDTH = 999
print( "Game Coordinates :", X_GAME, Y_GAME )

# finction location
# ==============================================================================================================
def waiting_for_my_turn():
#	pos_turn = locateOnScreen(images_dir + '/' + 'Plus2.png', grayscale=True, region=( X_GAME + 950, Y_GAME + 115, 45, 45 ), confidence=0.9)
	waiting_time = 0
	while locateOnScreen(images_dir + '/' + 'Plus2.png', grayscale=True, region=( X_GAME + 950, Y_GAME + 115, 45, 45 ), confidence=0.9) is None:
		print('its not my turn')
		waiting_time = waiting_time + 1
		if waiting_time == 5:
			print('check if im still in game')
			# pos = locateOnScreen(images_dir + '/' + 'GearLogo.png', grayscale=True, region=( X_GAME + 940, Y_GAME, 35, 25 ))
			if locateOnScreen(images_dir + '/' + 'GearLogo.png', grayscale=True, region=( X_GAME + 940, Y_GAME, 35, 25 )) is None:
				break
			else:
				print('still in game')
				sleep(0.5)
			waiting_time = 0
#		pos_turn = locateOnScreen(images_dir + '/' + 'Plus2.png', grayscale=True, region=( X_GAME + 950, Y_GAME + 115, 45, 45 ), confidence=0.9)

def special_event(turn, special_turn):
	if (turn % special_turn) == 0:
		for f in run_command:
			exec(f)

def get_angle():
	if path.exists('screenshot.png') is True:
		remove('screenshot.png')
	sleep(0.1)
	screenshot('screenshot.png', region=(X_GAME, Y_GAME, 1000, 600))

	for f in range(0,10):
		# print('scanning', f + 'x')
		angle_1 = locate(images_dir + '/' + str(f) + '.png', 'screenshot.png', region=( 38, 555, 12, 17), grayscale=True, confidence=0.9)
		if angle_1 is not None:
			angle_1 = f * 10
			break

	for g in range(0,10):
		# print('scanning', angle_1 + g )
		angle_2 = locate(images_dir + '/' + str(g) + '.png', 'screenshot.png', region=( 48, 555, 12, 17), grayscale=True, confidence=0.9)
		if angle_2 is not None:
			angle_2 = g
			break
	if (angle_1 is not None) and (angle_2 is not None):
		return(angle_1 + angle_2 )
	else:
		return(None)

def change_angle(wanted_angle):
	while True:
		current_angle = get_angle()
		print('current angle is :', current_angle)
		if (current_angle is not None) and (current_angle != wanted_angle):
			if current_angle < wanted_angle:
				press('w', presses=(wanted_angle - current_angle))
				break
			elif current_angle > wanted_angle:
				press('s', presses=(current_angle - wanted_angle))
				break
			elif current_angle == wanted_angle:
				break
		if current_angle is None:
			press('w', presses=wanted_angle)
		if current_angle == wanted_angle:
			break

def attack(force):
	pos1 = locateOnScreen(images_dir + '/' + 'pow.png', grayscale=True, region=( X_GAME + 920, Y_GAME + 515, 65, 60 ))
	if pos1 is not None:
		# no pow avail
		print('normal attack')
		press('1')
		press('2')
		keyDown('space')
		sleep(0.04 * force)
		press('4')
		keyUp('space')
	elif pos1 is None:
		# pow avail
		print('power attack')
		press('b')
		press('1')
		press('1')
		keyDown('space')
		sleep(0.04 * force)
		press('4')
		keyUp('space')

# ==============================================================================================================
#

# wating to enter the room
print('waiting to enter the game')
while locateOnScreen(images_dir + '/' + 'GearLogo.png', grayscale=True, region=( X_GAME + 940, Y_GAME, 35, 25 )) is None:
	print('still waiting...')
	sleep(1)
else:
	print('enterting the room')
sleep(waiting_at_the_begining)

	# all setup required here
print("setup direction, angle and power bar")
press('d')
click(x=X_GAME + 973, y=Y_GAME + 445)
print('check if you bring health kit')
if (str(special_turn) == 'start'):
	for f in run_command:
		exec(f)
print('setup angle to', angle)
change_angle(angle)

# attack
turn = 0
while locateOnScreen(images_dir + '/' + 'GearLogo.png', grayscale=True, region=( X_GAME + 940, Y_GAME, 35, 25 )) is not None:
	turn = turn + 1
	if (str(special_turn) != 'start'):
		special_event(turn, special_turn)
	attack(force)
	sleep(5)
	waiting_for_my_turn()
else:
	print("not in cave anymore")

