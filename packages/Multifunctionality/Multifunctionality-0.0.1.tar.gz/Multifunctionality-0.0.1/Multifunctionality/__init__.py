import keyboard
import time
import mouse
from playsound import playsound
def Autoclick(leftright='right', end='esc'):
    while True:
        mouse.click(leftright)
        if keyboard.is_pressed(end):
            break
        else:
            pass
def Call(a, b, *args):
    module = __import__(a)
    func = getattr(module, b)
    try:
        return func(*args)
    except TypeError:
        return func()
def Refresher(shortcut='ctrl + r', end='esc', a=5):
    while True:
        keyboard.send('ctrl + r')
        if keyboard.is_pressed('esc'):
            break
        else:
            time.sleep(a)
def Stopwatch(ext=False):
    print('start!')
    t = 0
    while True:
        print(t)
        if(keyboard.is_pressed('ctrl')):
            break
        else:
            time.sleep(1)
            t = t+1
    print('your time was:', t)
    time.sleep(5)
    if ext == True:
        exit()
def Timer(t, sound='Sound.wav', ext=False):
    print('start!')
    while t > 0:
        print(t)
        time.sleep(1)
        t = t-1
    while True:
        playsound(sound)
        if keyboard.is_pressed('Esc'):
            break     
        else:
            pass
    if ext == True:
        exit()
