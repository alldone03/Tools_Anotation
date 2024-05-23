import keyboard  # using module keyboard
import pyautogui
import time

def current_milli_time():
    return round(time.time() * 20)

first_delete = 189
delay_hold_keyboard= 7
while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('e'):  # if key 'q' is pressed 
            x,y = pyautogui.position()
            settime = current_milli_time()
            pyautogui.click(1075, 1020)
            pyautogui.moveTo(x,y)
            while keyboard.is_pressed('e'):
                pass
        elif keyboard.is_pressed('q'):
            x,y = pyautogui.position()
            settime = current_milli_time()
            pyautogui.click(843, 1023)
            pyautogui.moveTo(x,y)
            while keyboard.is_pressed('q'):
                pass
        elif keyboard.is_pressed('right'):
            x,y = pyautogui.position()
            settime = current_milli_time()
            pyautogui.click(1075, 1020)    
            pyautogui.moveTo(x,y)
            while keyboard.is_pressed('right'):
                pass
        elif keyboard.is_pressed('left'):
            x,y = pyautogui.position()
            settime = current_milli_time()
            pyautogui.click(843, 1023)
            pyautogui.moveTo(x,y)
            while keyboard.is_pressed('left'):
                pass
            
            
        elif keyboard.is_pressed('1'):
            x,y = pyautogui.position()
            settime = current_milli_time()
            while keyboard.is_pressed('1'):
                
                pass
            
            if not ((current_milli_time() - settime) < delay_hold_keyboard):
                pyautogui.click(1859, first_delete)
            else:
                pyautogui.click(1859-100, first_delete)
                x2,y2 = 1601,0
                while pyautogui.position().x >= x2:
                    # print(pyautogui.position().x, x2)
                    pass
            
            pyautogui.moveTo(x,y)
            
        elif keyboard.is_pressed('2'):
            x,y = pyautogui.position()
            settime = current_milli_time()
            
            
            while keyboard.is_pressed('2'):
                pass
            if not ((current_milli_time() - settime) < delay_hold_keyboard):
                pyautogui.click(1859, first_delete+40)
            else:
                pyautogui.click(1859-100, first_delete+40)
                x2,y2 = 1601,0
                while pyautogui.position().x >= x2:
                    pass
                 
            pyautogui.moveTo(x,y)
                 
                 
        elif keyboard.is_pressed('3'):
            x,y = pyautogui.position()
            settime = current_milli_time()
            
            
            while keyboard.is_pressed('3'):
                pass
            if not ((current_milli_time() - settime) < delay_hold_keyboard):
                pyautogui.click(1859, first_delete+40*2)
            else:
                pyautogui.click(1859-100, first_delete+40*2)
                x2,y2 = 1601,0
                while pyautogui.position().x >= x2:
                    pass
            pyautogui.moveTo(x,y)
            
            
        elif keyboard.is_pressed('4'):
            x,y = pyautogui.position()
            settime = current_milli_time()
            
            pyautogui.moveTo(x,y)
            while keyboard.is_pressed('4'):
                pass
            if not ((current_milli_time() - settime) < delay_hold_keyboard):
                pyautogui.click(1859, first_delete+40*3)
            else:
                pyautogui.click(1859-100, first_delete+40*3)
                x2,y2 = 1601,0
                while pyautogui.position().x >= x2:
                    pass
                 
            pyautogui.moveTo(x,y)
        elif keyboard.is_pressed('5'):
            x,y = pyautogui.position()
            settime = current_milli_time()
            
            pyautogui.moveTo(x,y)
            while keyboard.is_pressed('5'):
                pass
            if not ((current_milli_time() - settime) < delay_hold_keyboard):
                pyautogui.click(1859, first_delete+40*4)
            else :
                pyautogui.click(1859-100, first_delete+40*4)
                x2,y2 = 1601,0
                while pyautogui.position().x >= x2:
                    pass
            pyautogui.moveTo(x,y)
            
            
        elif keyboard.is_pressed('f'):
            x,y = pyautogui.position()
            settime = current_milli_time()
            pyautogui.moveTo(x,y)
            while keyboard.is_pressed('f'):
                pass
            if (current_milli_time() - settime) < 20:
                pass
            else:
                pass
    except:
        break  # if user pressed a key other than the given key the loop will break
    
    
