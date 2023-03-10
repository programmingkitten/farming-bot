import pyautogui
from textExtract import extractText
import numpy as np
import cv2
import time
import pytesseract
from PIL import Image
import pydirectinput
import subprocess
from dataValidators import isInt
from dataProcessing import removeUselessCharacters
coordOptions = {
    0: 'x',
    1: 'y',
    2: 'z',
}

currentCoords = {
    'x': 0,
    'y': 0,
    'z': 0,
}

state = 'forward'
stateKeys = {
    'forward': ['W', 'D'],
    'backward': ['S'],
    'switchToBackward': ['S', 'D'],
    'switchToForward': ['W', 'D']
}
farmPoints = {
    'forward': -142,
    'backward': 47
}

farmPoints[state]

farmCoords = [51, 71, 47]

def move(keys, keyUpAll=False):
    allKeys = ['W', 'A', 'S', 'D']
    if keyUpAll:
        for key2 in allKeys:
            pyautogui.keyUp(key2)
        pyautogui.mouseUp()
    for key in keys:
        print('keydown', key)
        pyautogui.keyDown(key)


time.sleep(3)
subprocess.run(["moveMouse.exe"])
lastCoords = []
while True:
    pic = pyautogui.screenshot(region=(320, 210, 290, 50))
    coords = pytesseract.image_to_string(pic)
    coords = coords.split(',')
    i = 0
    for coord in coords:
        
        coord = removeUselessCharacters(coord)
        coord = isInt(coord)
        if not coord:
            break

        coordType = coordOptions[i]
        currentCoords[f"{coordType}"] = coord
        print(currentCoords)
        print('STATE', farmPoints[state])

        if (currentCoords['x'] == 142 and currentCoords['z'] < -130):
            time.sleep(10000)

        if (coordType == 'z' and coord == farmPoints[state]):
            pyautogui.mouseUp()
            if state == 'forward':
                state = 'backward'
            else:
                state = 'forward'

            if state == 'backward':
                print('before')
                move(['S', 'D'], keyUpAll=True)
                time.sleep(3)
                move(stateKeys['backward'], keyUpAll=True)   
                pyautogui.mouseDown()    

            else:
                move(stateKeys['forward'], keyUpAll=True)
                time.sleep(3.5)
                pyautogui.mouseDown()    
            pass

        i += 1

    lastCoords.append(currentCoords['z'])
    if len(lastCoords) >= 6:
        repeatedCoords = lastCoords.count(lastCoords[0])
        if repeatedCoords > 3:
            pyautogui.mouseUp()
            move('A', keyUpAll=True)
            time.sleep(2)
            move(stateKeys[state], keyUpAll=True)
            pyautogui.mouseDown()
        repeatedCoords = []
        
        
    time.sleep(0.1)