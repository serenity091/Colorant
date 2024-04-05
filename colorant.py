import sys
import os
import cv2
import numpy as np
import threading
import time
import win32api
import pyautogui
import configparser
import random


from termcolor import colored
from capture import Capture
from mouse import Mouse
from settings import Settings

class Colorant:
    settings = Settings()

    def __init__(self, x, y, xfov, yfov):
        self.settings = Settings()
        self.mouse = Mouse()
        self.grabber = Capture(x, y, xfov, yfov)
        self.LOWER_COLOR, self.UPPER_COLOR = self.get_colors()
        self.toggled = False
        self.configure()

    def configure(self):
        try:
            self.SENSITIVITY = self.settings.get_float('Settings', 'VALORANT-SENSITIVITY')
            self.FLICKSPEED = 1.07437623 * (self.SENSITIVITY ** -0.9936827126)
            
            if self.settings.get_boolean('AIMBOT', 'RANDOM-SPEED'):
                x_random_range = self.settings.get_float_list('AIMBOT', 'X-RANDOM')
                y_random_range = self.settings.get_float_list('AIMBOT', 'Y-RANDOM')
                self.xspeed = lambda: random.uniform(x_random_range[0], x_random_range[1])
                self.yspeed = lambda: random.uniform(y_random_range[0], y_random_range[1])

            else:
                self.xspeed = lambda: self.settings.get_float('AIMBOT', 'X-SPEED')
                self.yspeed = lambda: self.settings.get_float('AIMBOT', 'Y-SPEED')
            
            self.AIMBOT_KEY = int(self.settings.get('AIMBOT', 'KEY-BIND'), 16)
            self.TRIGGERBOT_KEY = int(self.settings.get('TRIGGERBOT', 'KEY-BIND'), 16)
            self.SILENTBOT_KEY = int(self.settings.get('SILENTBOT', 'KEY-BIND'), 16)
            self.TOGGLE_KEY = int(self.settings.get('Settings', 'COLORANT-TOGGLE'), 16)
        except:
            os.system('cls')
            print(colored('[Error]', 'red'), colored('Invalid value found in settings.ini', 'white'))
            time.sleep(10)
            sys.exit()

    def get_colors(self):
        if self.settings.get('Settings', 'PLAYER-COLOR') == "PURPLE":
            lower_color = np.array([140, 120, 180])
            upper_color = np.array([160, 200, 255])
        elif self.settings.get('Settings', 'PLAYER-COLOR') == "YELLOW":
            lower_color = np.array([30, 125, 150])
            upper_color = np.array([30, 255, 255])
        elif self.settings.get('Settings', 'PLAYER-COLOR') == "RED":
            lower_color = np.array([30, 150, 220])
            upper_color = np.array([190, 190, 250])
        else:
            os.system('cls')
            print(colored('[Error]', 'red'), colored('Invalid value found in settings.ini', 'white'))
            time.sleep(10)
            sys.exit()
        return lower_color, upper_color

    def toggle(self):
        self.toggled = not self.toggled
        time.sleep(0.2)
        
    def listen(self):
        key_pressed = False
        status = 'Disabled'
        print(f'{colored("[Status]", "white", "on_light_red")}', end='\n')
        while True:
            if win32api.GetAsyncKeyState(self.AIMBOT_KEY) < 0 and self.toggled and self.settings.get_boolean('AIMBOT', 'ENABLED'):
                self.process("move")
            elif win32api.GetAsyncKeyState(self.TRIGGERBOT_KEY) < 0 and self.toggled and self.settings.get_boolean('TRIGGERBOT', 'ENABLED'):
                self.process("click")  
            elif win32api.GetAsyncKeyState(self.SILENTBOT_KEY) < 0 and self.toggled and self.settings.get_boolean('SILENTBOT', 'ENABLED'):
                if not key_pressed:
                    self.process("flick")
                key_pressed = True
            else:
                key_pressed = False

            if win32api.GetAsyncKeyState(self.TOGGLE_KEY) < 0:
                self.toggle()
                status = 'Enabled \b' if self.toggled else 'Disabled'
            print(f'\r{colored(status, "white")}', end='')

    def process(self, action):
        hsv = cv2.cvtColor(self.grabber.get_screen(), cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.LOWER_COLOR, self.UPPER_COLOR)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if contours:
            screen_center = (self.grabber.xfov // 2, self.grabber.yfov // 2)
            min_distance = float('inf')
            closest_contour = None

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                center = (x + w // 2, y + h // 2)
                distance = ((center[0] - screen_center[0]) ** 2 + (center[1] - screen_center[1]) ** 2) ** 0.5

                if distance < min_distance:
                    min_distance = distance
                    closest_contour = contour

            x, y, w, h = cv2.boundingRect(closest_contour)
            center = (x + w // 2, y + h // 2)
            cX = center[0]
            cY = y + int(h * float(self.settings.get('Settings', 'TARGET-LOCATION')))
            cYcenter = center[1] - self.grabber.yfov // 2
            x_diff = cX - self.grabber.xfov // 2
            y_diff = cY - self.grabber.yfov // 2

            if action == "move":
                self.mouse.move(self.xspeed() * x_diff, self.yspeed() * y_diff)

            elif action == "click":
                x_threshold = self.settings.get_int('TRIGGERBOT', 'X_THRESHOLD')
                y_threshold = self.settings.get_int('TRIGGERBOT', 'Y_THRESHOLD')
                if abs(x_diff) <= x_threshold and abs(cYcenter) <= y_threshold:
                    time.sleep(self.settings.get_float('TRIGGERBOT', 'DELAY-BEFORE-SHOOT'))
                    self.mouse.click()
                    time.sleep(self.settings.get_float('TRIGGERBOT', 'DELAY-AFTER-SHOOT'))

            elif action == "flick":
                xflick = x_diff * self.FLICKSPEED
                yflick = y_diff * self.FLICKSPEED
                self.mouse.move(xflick, yflick)
                self.mouse.click()
                if not self.settings.get_boolean('SILENTBOT', 'ONLY-FLICK'):
                    self.mouse.move(-(xflick), -(yflick))
