import cv2
import time
import numpy as np
import pyautogui
from pyscreeze import screenshot

from auto_gui import text_detection, super_resolution, error, browser

CLICK_COMMAND = "click"
MOVE_COMMAND = "move"
DOUBLE_CLICK_COMMAND = "double_click"
WRITE_COMMAND = "write"
OPEN_BROWSER_COMMAND = "open_browser"
SLEEP_COMMAND = "sleep"
PRESS_COMMAND = "press"
HOT_KEY_COMMAND = "hot_key"

class Command(object):
    def __init__(self, **data):
        self.command = data.get("command")
        self.params = data.get("params")
        self.screen_width, self.screen_height = pyautogui.size()

    def exec(self):
        if self.command == CLICK_COMMAND:
            self.click()
        elif self.command == MOVE_COMMAND:
            self.move()
        elif self.command == DOUBLE_CLICK_COMMAND:
            self.double_click()
        elif self.command == WRITE_COMMAND:
            self.write()
        elif self.command == OPEN_BROWSER_COMMAND:
            self.open_browser()
        elif self.command == SLEEP_COMMAND:
            self.sleep()
        elif self.command == PRESS_COMMAND:
            self.press()
        elif self.command == HOT_KEY_COMMAND:
            self.hot_key()
        else:
            raise Exception(error.COMMAND_NOT_FOUND)

    def click(self):
        len_params = len(self.params)
        if len_params == 0:
            pyautogui.click()
        elif len_params == 1:
            self.handle_text_screenshot()
        elif len_params == 2:
            pyautogui.click(self.params[0], self.params[1])
        else:
            raise Exception(error.INVALID_COMMAND_PARAMS)

    def move(self):
        len_params = len(self.params)
        if len_params == 1:
            self.handle_text_screenshot()
        elif len_params == 2:
            if self.params[0] == None or self.params[0] == None:
                pyautogui.move(self.params[0], self.params[1])
            else:
                pyautogui.moveTo(self.params[0], self.params[1])
        else:
            raise Exception(error.INVALID_COMMAND_PARAMS)

    def double_click(self):
        len_params = len(self.params)
        if len_params == 0:
            pyautogui.doubleClick()
        elif len_params == 1:
            self.handle_text_screenshot()
        elif len_params == 2:
            pyautogui.doubleClick(self.params[0], self.params[1])
        else:
            raise Exception(error.INVALID_COMMAND_PARAMS)

    def write(self):
        len_params = len(self.params)
        if len_params == 1:
            pyautogui.write(self.params[0])
        else:
            raise Exception(error.INVALID_COMMAND_PARAMS)

    def open_browser(self):
        len_params = len(self.params)
        if len_params == 1:
            browser.Browser(url=self.params[0]).open()
        elif len_params == 2:
            browser.Browser(browser=self.params[0], url=self.params[1]).open()
        else:
            raise Exception(error.INVALID_COMMAND_PARAMS)

    def sleep(self):
        len_params = len(self.params)
        if len_params == 1:
            time.sleep(int(self.params[0]))
        else:
            raise Exception(error.INVALID_COMMAND_PARAMS)

    def press(self):
        len_params = len(self.params)
        if len_params == 1:
            pyautogui.press(self.params[0])
        else:
            raise Exception(error.INVALID_COMMAND_PARAMS)

    def hot_key(self):
        pyautogui.hotkey(*self.params)

    def handle_text_screenshot(self):
        img = self.get_screen_shot()

        img = super_resolution.SuperResolution(img=img).scale()

        cv2.imwrite("output.png", img)

        text_positions = text_detection.TextDetection(
            img=img).get_text_positions(self.params[0])

        if len(text_positions) == 0:
            raise Exception(error.TEXT_NOT_FOUND)

        if self.command == CLICK_COMMAND:
            pyautogui.click(round(text_positions[0][0] / 2), round(text_positions[0][1] / 2))
        elif self.command == MOVE_COMMAND:
            pyautogui.moveTo(round(text_positions[0][0] / 2), round(text_positions[0][1] / 2))
        elif self.command == DOUBLE_CLICK_COMMAND:
            pyautogui.doubleClick(round(text_positions[0][0] / 2), round(text_positions[0][1] / 2))

    def get_screen_shot(self):
        # screen_shot = screenshot(command="flameshot", command_params=["screen"])
        screen_shot = screenshot(command="scrot", command_params=["-z"])
        screen_shot_numpy = np.array(screen_shot)
        return cv2.cvtColor(screen_shot_numpy, cv2.COLOR_RGB2BGR)
