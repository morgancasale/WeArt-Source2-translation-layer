import time
import json
import pyautogui
from PIL import Image


models = json.load(open("updated_model_materials_with_imgs.json"))

#pyautogui.moveTo(175, 140)
# im = pyautogui.screenshot(region=(610, 115, 350, 450))
# im.show()


for model in models:
    if(model["prob"] < 100):
        pyautogui.moveTo(175, 140)
        pyautogui.click()
        pyautogui.hotkey('ctrl','a')
        pyautogui.typewrite(model["model"], interval=0.002)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.moveTo(175, 400)
        pyautogui.click()        
        time.sleep(2)

        name = model["model"].split("/")[-1].split(".")[0]
        im = pyautogui.screenshot("screens\\" + name + ".png", region=(610, 115, 350, 450))

        


#pyautogui.click()