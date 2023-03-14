import time

import cv2
import numpy as np
import pyautogui
import pyscreeze

from .text_detection import TextDetection
from .match_template import MatchTemplate
from .super_resolution import SuperResolution
from .error import COMMAND_NOT_FOUND, INVALID_COMMAND_PARAMS, TEXT_NOT_FOUND, TEMPLATE_NOT_FOUND
from .browser import Browser

CLICK_COMMAND = "click"
MOVE_COMMAND = "move"
DOUBLE_CLICK_COMMAND = "double_click"
WRITE_COMMAND = "write"
OPEN_BROWSER_COMMAND = "open_browser"
SLEEP_COMMAND = "sleep"
PRESS_COMMAND = "press"
HOT_KEY_COMMAND = "hot_key"
TEXT_SUBCOMMAND = "text"
TEMPLATE_SUBCOMMAND = "template"

class Command(object):
    def __init__(self, **data):
        self.command = data.get("command")
        self.params = data.get("params")

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
            raise Exception(COMMAND_NOT_FOUND)

    def click(self):
        len_params = len(self.params)
        if len_params == 0:
            pyautogui.click()
        elif len_params == 2:
            if self.params[0] == TEXT_SUBCOMMAND:
                self.handle_text_screenshot(self.params[1])
            elif self.params[0] == TEMPLATE_SUBCOMMAND:
                self.handle_template_screenshot(self.params[1])
            else:
                if type(self.params[0]) == str:
                    self.params[0] = int(self.params[0])

                if type(self.params[1]) == str:
                    self.params[1] = int(self.params[1])

                pyautogui.click(self.params[0], self.params[1])
        else:
            raise Exception(INVALID_COMMAND_PARAMS)

    def move(self):
        if len(self.params) == 2:
            if self.params[0] == TEXT_SUBCOMMAND:
                self.handle_text_screenshot(self.params[1])
            elif self.params[0] == TEMPLATE_SUBCOMMAND:
                self.handle_template_screenshot(self.params[1])
            elif self.params[0] == None or self.params[0] == None:
                if type(self.params[0]) == str:
                    self.params[0] = int(self.params[0])

                if type(self.params[1]) == str:
                    self.params[1] = int(self.params[1])

                pyautogui.move(self.params[0], self.params[1])
            else:
                if type(self.params[0]) == str:
                    self.params[0] = int(self.params[0])

                if type(self.params[1]) == str:
                    self.params[1] = int(self.params[1])

                pyautogui.moveTo(self.params[0], self.params[1])
        else:
            raise Exception(INVALID_COMMAND_PARAMS)

    def double_click(self):
        len_params = len(self.params)
        if len_params == 0:
            pyautogui.doubleClick()
        elif len_params == 2:
            if self.params[0] == TEXT_SUBCOMMAND:
                self.handle_text_screenshot(self.params[1])
            elif self.params[0] == TEMPLATE_SUBCOMMAND:
                self.handle_template_screenshot(self.params[1])
            else:
                if type(self.params[0]) == str:
                    self.params[0] = int(self.params[0])

                if type(self.params[1]) == str:
                    self.params[1] = int(self.params[1])

                pyautogui.doubleClick(self.params[0], self.params[1])
        else:
            raise Exception(INVALID_COMMAND_PARAMS)

    def write(self):
        if len(self.params) == 1:
            pyautogui.write(self.params[0])
        else:
            raise Exception(INVALID_COMMAND_PARAMS)

    def open_browser(self):
        len_params = len(self.params)
        if len_params == 1:
            Browser(url=self.params[0]).open()
        elif len_params == 2:
            Browser(browser=self.params[0], url=self.params[1]).open()
        else:
            raise Exception(INVALID_COMMAND_PARAMS)

    def sleep(self):
        if len(self.params) == 1:
            if type(self.params[0]) == str:
                self.params[0] = int(self.params[0])
                
            time.sleep(self.params[0])
        else:
            raise Exception(INVALID_COMMAND_PARAMS)

    def press(self):
        if len(self.params) == 1:
            pyautogui.press(self.params[0])
        else:
            raise Exception(INVALID_COMMAND_PARAMS)

    def hot_key(self):
        pyautogui.hotkey(*self.params)

    def handle_text_screenshot(self, text):
        img = self.get_screen_shot()

        img = SuperResolution(img=img).scale()

        text_positions = TextDetection(
            img=img).get_text_positions(text)

        if len(text_positions) == 0:
            raise Exception(TEXT_NOT_FOUND)

        if self.command == CLICK_COMMAND:
            pyautogui.click(round(text_positions[0][0] / 2), round(text_positions[0][1] / 2))
        elif self.command == MOVE_COMMAND:
            pyautogui.moveTo(round(text_positions[0][0] / 2), round(text_positions[0][1] / 2))
        elif self.command == DOUBLE_CLICK_COMMAND:
            pyautogui.doubleClick(round(text_positions[0][0] / 2), round(text_positions[0][1] / 2))

    def handle_template_screenshot(self, path):
        screen_shot = self.get_screen_shot()
        template = cv2.imread(path)

        positions = MatchTemplate(img=screen_shot).get_template_positions(template)

        if len(positions) == 0:
            raise Exception(TEMPLATE_NOT_FOUND)

        if self.command == CLICK_COMMAND:
            pyautogui.click(round(positions[0][0] / 2), round(positions[0][1] / 2))
        elif self.command == MOVE_COMMAND:
            pyautogui.moveTo(round(positions[0][0] / 2), round(positions[0][1] / 2))
        elif self.command == DOUBLE_CLICK_COMMAND:
            pyautogui.doubleClick(round(positions[0][0] / 2), round(positions[0][1] / 2))

    def get_screen_shot(self):
        # screen_shot = screenshot(command="flameshot", command_params=["screen"])
        screen_shot = pyscreeze.screenshot(command="scrot", command_params=["-z"])
        return cv2.cvtColor(np.array(screen_shot), cv2.COLOR_RGB2BGR)
