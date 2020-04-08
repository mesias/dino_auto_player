import os
import time
import pyautogui
import subprocess
import threading
import pytesseract
import mss
from PIL import Image
from datetime import datetime, timedelta
import pyscreenshot as ImageGrab

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

chrome_params = ['/usr/bin/google-chrome', '--new-window', '--profile-directory=Default', '--guest']

def get_delta():
    total_elapsed = time.time() - ttt
    return timedelta(seconds=total_elapsed)

def execute_chrome():
    p = subprocess.Popen(chrome_params)
    time.sleep(0.5)

def get_highscore(retry, total):
    time = datetime.now()
    #filename = 'dino/scn-{:%Y%m%d_%H%M%S}-{:02d}-{:05d}-score.png'.format(time, retry, total)
    #answer = pyautogui.screenshot(filename ,region=(1200, 200, 150, 50))
    filename = 'dino/scn-{:%Y%m%d_%H%M%S}-{:02d}-{:05d}-full.png'.format(time, retry, total)
    answer = pyautogui.screenshot(filename)
    print('Screenshot', answer, time)
    # img = Image.open(filename)
    # val = pytesseract.image_to_string(img, config='-psm 6')
    # print('Found score: ', val)

execute_chrome()

#abrir o jogo
pyautogui.hotkey('ctrl', 'l')
pyautogui.write('chrome://dino')
pyautogui.press('enter')
time.sleep(1)

#iniciar

pyautogui.press('up')
ttt = time.time()
time.sleep(1.5)

locateBorder = pyautogui.locateOnScreen('img/dino_chrome_border_min.png', grayscale=True)
print('Border', locateBorder)

zero_left = locateBorder.left - 18
zero_top = locateBorder.top - 5

region_pos = ((zero_left + 380), (zero_top + 390), 1, 150)
grab_pos = (region_pos[0], region_pos[1], region_pos[0]+region_pos[2], region_pos[1]+region_pos[3])
grab_dino = ((zero_left + 90), (zero_top + 480), (zero_left + 110), (zero_top + 480))

grab_all = ((zero_left + 90), (zero_top + 390), region_pos[0]+region_pos[2], region_pos[1]+region_pos[3])
grey_color = (83, 83, 83)
ggrey_color = (172, 172, 172)
grey_tuple = (grey_color, ggrey_color)
screen_shot_min_highscore = 700
sct = mss.mss()
running = True
tdata = None
jump = False
jump_count_grey = 0
jump_count_grey_total = 0
jump_count_white = 0

pyautogui.moveTo(*grab_all[-2:])

def check_pix(pos):
    try:
        pix_down = pyautogui.pixelMatchesColor(pos[0], pos[1],
            grey_color, tolerance=20)
        return pix_down
    except Exception as e:
        print(e)
        return False

def get_data(pixels, pixel_background):
    counter = 0
    lst = []
    last = -1
    frst = -1
    size = 0
    for i, p in enumerate(pixels):
        if p != pixel_background:
            if last > 0 and (last + 1) == i:
                if frst < 0:
                    frst = i
                size += 1
            counter += 1
            last = i
        elif frst > 0:
            lst.append((frst,size, frst+size))
            size = 0
            frst = -1
    if not lst and size > 0:
        lst.append((frst, size, size))

    return counter, lst

print('running')
last_jump = -1
retry = 20
count = -1
sw = True
while running:
    count += 1
    up = dw = None
    mytime = int((time.time() - ttt) * 10)

    # up = check_pix(pos_down)
    # da = pyautogui.screenshot( region=region_pos)    
    da = sct.grab(grab_all)
    pixel_background = da.pixel(0,region_pos[3]-1)
    if not jump:
        pixels, lst = get_data([da.pixel(da.width-1,i) for i in range(100)], pixel_background)
    else:
        pixels, lst = 0, []
        #pixels_dino = list(filter(lambda x: x != (255, 255, 255), conv_to_rgb(da)))
        pixels_dino = da.pixel(0,90)

        if pixels_dino != pixel_background:
            jump_count_grey += 1
            jump_count_grey_total += 1
            #print('Dino jump', jump_count_grey, jump_count_white)
        else:
            jump_count_grey = 0
        jump_count_white += 1
        if jump_count_grey >= 8:
            print('Aterrisou G[{}:{}] W[{}]'.format(jump_count_grey, 
                jump_count_grey_total-jump_count_grey, jump_count_white))
            jump = False
            jump_count_grey_total = jump_count_grey = jump_count_white = 0
    # if pixels > 2:
    #     print('Wall:', pixels, ':', lst)

    if pixels > 6:
        print(retry, 'jump', pixels, lst, 'time:', mytime)
        pyautogui.press('up')
        jump = True
        jump_count_grey = jump_count_white = 0
        last_jump = time.time()

    if last_jump > 0:
        elap = time.time() - last_jump
        if elap > 3:
            total_time = int((time.time() - ttt) * 10)
            if total_time > screen_shot_min_highscore:
                get_highscore(retry, total_time)
            else:
                print("LOW HIGSCORE: {}".format(total_time))
            if retry > 0:
                print('Retry:{} elap:{} total:{}'.format(retry, elap, total_time))
                # print(pytesseract.image_to_string(img, config='-psm 6'))
                # print('Tesseract ', pytesseract.image_to_string(img, config='-psm 6'))
                last_jump = -1
                retry -= 1
                pyautogui.press('enter')
                ttt = time.time()
            else:
                running = False

    time.sleep(0.001)