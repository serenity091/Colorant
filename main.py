# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.16 (default, Mar  2 2023, 03:18:16) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: main.py
import os, sys, time, win32api, pyautogui, ctypes, threading, hashlib
from datetime import datetime
from termcolor import colored
from colorant import Colorant
from settings import Settings
# from keyauth import api

class Main:
    os.system('color')
    KEY_NAMES = {
      1: 'L Mouse Button',  2: 'R Mouse Button',  4: 'MButton',  5: 'X1 Mouse Button',
      6: 'X2 Mouse Button',  8: 'Backspace',  9: 'Tab',  13: 'Enter',  16: 'Shift',
      17: 'Ctrl',  18: 'Alt',  20: 'CapsLock',  27: 'Esc',  32: 'Spacebar',  37: 'Left',
      38: 'Up',  39: 'Right',  40: 'Down',  48: '0',  49: '1',  50: '2',  51: '3',
      52: '4',  53: '5',  54: '6',  55: '7',  56: '8',  57: '9',  65: 'A',  66: 'B',
      67: 'C',  68: 'D',  69: 'E',  70: 'F',  71: 'G',  72: 'H',  73: 'I',  74: 'J',
      75: 'K',  76: 'L',  77: 'M',  78: 'N',  79: 'O',  80: 'P',  81: 'Q',  82: 'R',
      83: 'S',  84: 'T',  85: 'U',  86: 'V',  87: 'W',  88: 'X',  89: 'Y',  90: 'Z',
      112: 'F1',  113: 'F2',  114: 'F3',  115: 'F4',  116: 'F5',  117: 'F6',
      118: 'F7',  119: 'F8',  120: 'F9',  121: 'F10',  122: 'F11',  123: 'F12'}

    def __init__(self):
        self.settings = Settings()
        self.monitor = pyautogui.size()
        self.CENTER_X, self.CENTER_Y = self.monitor.width // 2, self.monitor.height // 2
        self.XFOV = self.settings.get_int('Settings', 'X-FOV')
        self.YFOV = self.settings.get_int('Settings', 'Y-FOV')
        self.colorant = Colorant(self.CENTER_X - self.XFOV // 2, self.CENTER_Y - self.YFOV // 2, self.XFOV, self.YFOV)

    def get_checksum(self):
        md5_hash = hashlib.md5()
        file = open(''.join(sys.argv), 'rb')
        md5_hash.update(file.read())
        digest = md5_hash.hexdigest()
        return digest

    def authenticate(self):
        self.keyauthapp = api(name='Colorant',
          ownerid='XpXJiuVsQu',
          secret='5f3628628bc9a1261189c940d38278905ad42ecbea7286f54a38ddab8966f5b0',
          version='1.4',
          hash_to_check=(self.get_checksum()))
        key = self.settings.get('Settings', 'AUTH-KEY')
        if not key:
            key = input(colored('[Auth]', 'white', 'on_light_red') + colored(' Please Enter your Key: ', 'light_red'))
            self.settings.set('Settings', 'AUTH-KEY', key)
            self.settings.save()
        self.keyauthapp.license(key)
        APP_NAME = self.settings.get('Settings', 'APP-NAME')
        os.system(f"title {APP_NAME}")
        os.system('cls')
        print(colored(' \t\t\t\t  Welcome Back! ● Expiry ' + datetime.utcfromtimestamp(int(self.keyauthapp.user_data.expires)).strftime('%Y-%m-%d at %#H:%M %p'), 'light_red'))

    def better_cmd(self, width, height):
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
            style &= -262145
            style &= -65537
            ctypes.windll.user32.SetWindowLongW(hwnd, -16, style)
        STD_OUTPUT_HANDLE_ID = ctypes.c_ulong(4294967285)
        windll = ctypes.windll.kernel32
        handle = windll.GetStdHandle(STD_OUTPUT_HANDLE_ID)
        rect = ctypes.wintypes.SMALL_RECT(0, 0, width - 1, height - 1)
        windll.SetConsoleScreenBufferSize(handle, ctypes.wintypes._COORD(width, height))
        windll.SetConsoleWindowInfo(handle, ctypes.c_int(True), ctypes.pointer(rect))

    def print_logo(self):
        print(colored('\n                     ▄▄·       ▄▄▌        ▄▄▄   ▄▄▄·  ▐ ▄ ▄▄▄▄▄     ▄▄▄·▄▄▌  ▄• ▄▌.▄▄ · \n                    ▐█ ▌▪▪     ██•  ▪     ▀▄ █·▐█ ▀█ •█▌▐█•██      ▐█ ▄███•  █▪██▌▐█ ▀. \n                    ██ ▄▄ ▄█▀▄ ██▪   ▄█▀▄ ▐▀▀▄ ▄█▀▀█ ▐█▐▐▌ ▐█.▪     ██▀·██▪  █▌▐█▌▄▀▀▀█▄\n                    ▐███▌▐█▌.▐▌▐█▌▐▌▐█▌.▐▌▐█•█▌▐█ ▪▐▌██▐█▌ ▐█▌·    ▐█▪·•▐█▌▐▌▐█▄█▌▐█▄▪▐█\n                    ·▀▀▀  ▀█▄▀▪.▀▀▀  ▀█▄▀▪.▀  ▀ ▀  ▀ ▀▀ █▪ ▀▀▀     .▀   .▀▀▀  ▀▀▀  ▀▀▀▀ \n                                                  v1.4', 'light_red'))

    def print_info(self):
        try:
            print(colored('[Your Keybinds]', 'white', 'on_light_red'))
            print(colored(f"[x] Hold ({self.KEY_NAMES[self.colorant.AIMBOT_KEY]})", 'light_red'), colored('→ Aimbot', 'white'))
            print(colored(f"[x] Hold ({self.KEY_NAMES[self.colorant.TRIGGERBOT_KEY]})", 'light_red'), colored('→ Triggerbot', 'white'))
            print(colored(f"[x] Press ({self.KEY_NAMES[self.colorant.SILENTBOT_KEY]}) Warning high detection", 'light_red'), colored('→ Silentaim\n', 'white'))
            print(colored('[Information]', 'white', 'on_light_red'))
            print(colored('Set enemies to', 'white'), colored('Purple', 'light_red'))
            print(colored(f"Press {colored(self.KEY_NAMES[self.colorant.TOGGLE_KEY], 'light_red')} to toggle ON/OFF Colorant", 'white'))
            print(colored('Thanks again for your support, welcome to ', 'white') + colored('COLORANT', 'light_red') + colored(' family!\n', 'white'))
        except:
            os.system('cls')
            print(colored('[Error]', 'red'), colored('Invalid value found in settings.ini', 'white'))
            time.sleep(10)
            sys.exit()

    def run(self):
        self.better_cmd(120, 30)
        #self.authenticate()
        self.print_logo()
        self.print_info()
        self.colorant.listen()


if __name__ == '__main__':
    Main().run()