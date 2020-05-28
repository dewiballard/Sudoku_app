#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 17:13:06 2020

@author: dewiballard
"""
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import re
import os

class PuzzleSelector(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
        self.add_widget(Label(text='Sudoku solver app'))
        
        self.easy = Button(text='Easy (2x3)')
        self.add_widget(self.easy)
        self.medium = Button(text='Medium (3x3)')
        self.add_widget(self.medium)
        self.medium.bind(on_press=self.Grid_button)
        self.hard1 = Button(text='Hard1 (3x4)')
        self.add_widget(self.hard1)
        self.hard2 = Button(text='Hard2 (4x3)')
        self.add_widget(self.hard2)
        self.extreme = Button(text='Extreme (4x4)')
        self.add_widget(self.extreme)
    
    def Grid_button(self, instance):
        info = f'Attempting to configure your grid, please enter your known values...'
        PuzzleApp.info_page.update_info(info)
        PuzzleApp.screen_manager.current = 'Info'
        Clock.schedule_once(self.grid, 3)
    
    def grid(self, _):        
        PuzzleApp.create_grid()
        PuzzleApp.screen_manager.current = 'Grid'
        

class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign='center', valign='middle', font_size=60)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)
    def update_info(self, message):
        self.message.text = message
    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)

class GridPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 9                                           # This values needs to be updated for each grid type
        
        for i in range(81):                                     # This values needs to be updated for each grid type
            self.name = FloatInput(multiline=False)
            self.add_widget(self.name)

#MAKE BOLD LINES ACROSS GRID BOUNDARIES - MAYBE NOT BOTHER IF IT'S GOING TO READ BY PICTURE
# For next (solver part), assume 0 if empty...

class FloatInput(TextInput):                                    # Could do with increasing font size

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '[^0-9]' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '[^0-9]'.join([re.sub(pat, '', s) for s in substring.split('[^0-9]', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

class EpicApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        
        self.puzzle_selector = PuzzleSelector()        
        screen = Screen(name='Connect')
        screen.add_widget(self.puzzle_selector)
        self.screen_manager.add_widget(screen)
        
        self.info_page = InfoPage()
        screen = Screen(name='Info')
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager

    def create_grid(self):
        self.grid_page = GridPage()
        screen = Screen(name='Grid')
        screen.add_widget(self.grid_page)
        self.screen_manager.add_widget(screen)
        
    
if __name__ == '__main__':
    PuzzleApp = EpicApp()
    PuzzleApp.run()
    