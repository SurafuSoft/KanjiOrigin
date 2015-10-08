#!/usr/bin/kivy
# -*- coding: utf-8 -*-

#import os
from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
#from kivy.uix.behaviors import FocusBehavior
#from kivy.metrics import dp
#import csv

from kivy.utils import platform
import data.screens.learnkanji_k_alg as lrnalg


class KanjiOriginScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(KanjiOriginScreen, self).add_widget(*args)


class KanjiOriginApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    screen_names = ListProperty([])
    actionbar_status = ListProperty([0, 0, 0, 0])

    def build(self):
        self.title = 'Kanji Origin'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = ([
            'MainMenu', 'LearnKanji_k', 'LearningMethod', 'Backup', 'Donation', 'Credits'])
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
            '{}.kv'.format(fn)) for fn in self.available_screens]
        self.go_screen(0)

        # Binds the back button on Android
        self.bind(on_start=self.post_build_init)

        # Status bar
        try:
            self.learnalg_count = lrnalg.LearnCount()
            if self.learnalg_count.db_exist:
                self.actionbar_status = self.learnalg_count.countlearned()
            else:
                self.actionbar_status = [-1, -1, -1, -1]

        except:
            print("Database error or learnkanji_k_alg.py not found")

    # Binds the back button on Android
    def post_build_init(self, *args):
        # if platform() == 'android':
        #     import android
        #     android.map_key(android.KEYCODE_BACK, 1001)

        win = Window
        win.bind(on_keyboard=self.my_key_handler)

    def my_key_handler(self, window, keycode1, keycode2, text, modifiers):
        # Esc or Android back button pressed
        if keycode1 in [27, 1001]:
            # Keyboard open -> close it
            #if Window.keyboard_height > dp(25):
            #    window.close()

            # if FocusBehavior._keyboards and any(FocusBehavior._keyboards.values()):
            #     print(FocusBehavior._keyboards.values())


            # Not in main screen
            print("self.index: {}".format(self.index))
            if self.index != 0:
                print("self.index not 0")
                self.go_screen(0)
                return True
            # In main screen
            else:
                print("self.index 0")
                print("Closing App")
                App.get_running_app().stop()

        return False

    def on_pause(self):
        return True

    def on_resume(self):
        if self.learnalg_count:
            if self.learnalg_count.db_exist:
                self.actionbar_status = self.learnalg_count.countlearned()

    def go_screen(self, idx):
        self.index = idx
        if idx == 0:
            self.root.ids.sm.switch_to(self.load_screen(idx), direction='right')
        else:
            # Only load learnkanji.py when the screen is called
            #if idx == 1:
            #    import data.screens.learnkanji
            self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index].lower())
        self.screens[index] = screen
        return screen

    def _update_clock(self, dt):
        self.time = time()

if __name__ == '__main__':
    KanjiOriginApp().run()