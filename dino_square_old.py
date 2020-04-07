import os
import time
import pyautogui
import subprocess
import threading
from datetime import datetime, timedelta

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

ttt = time.time()

def get_delta():
    total_elapsed = time.time() - ttt
    return timedelta(seconds=total_elapsed)

def execute_chrome():
    p = subprocess.Popen("pwd")
    time.sleep(0.5)

chrome://dino_reset
#abrir o jogo
pyautogui.hotkey('ctrl', 'l')
pyautogui.write('chrome://dino')
pyautogui.press('enter')
time.sleep(0.2)

#iniciar

pyautogui.press('up')
time.sleep(1)

pos_down = (300, 470)
pos_up = (300, 400)
grey_color = (83, 83, 83)
global running
running = True

pyautogui.moveTo(*pos_up)

def check_pix(pos):
    try:
        # pix = pyautogui.pixel(*position_down)
        pix_down = pyautogui.pixelMatchesColor(pos[0], pos[1],
            grey_color, tolerance=20)
        return pix_down
    except Exception as e:
        print(e)
        return False

def thread_function():
    global running
    while running:
        if check_pix(pos_down):
            print('jump')
            pyautogui.press('up')
        time.sleep(0.00001)

def thread_check():
    global running
    print('Thead check')
    while running:
        if check_pix(pos_up):
            print('down')
        time.sleep(0.00001)

x = threading.Thread(target=thread_function)
# y = threading.Thread(target=thread_check)
x.start()
# y.start()
print('running')


try_game = 3
while running:
    locateSuccess = pyautogui.locateOnScreen('dino_reset.png', grayscale=True)
    if locateSuccess:
        if try_game > 0:
            pyautogui.press('enter')
        else:
            running = False
        try_game -= 1
        print('Game stop:', try_game)
    time.sleep(0.0001)
print('Finishing run')
# y.join()
x.join()

    # if check_pix(pos_up):
    #     print('down')
    #     pyautogui.press('down')

# locateSuccess = pyautogui.locateOnScreen('batida_sucesso.png', grayscale=True)






