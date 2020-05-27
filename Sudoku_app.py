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
import os

class PuzzleSelector(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
        self.add_widget(Label(text='Welcome to the ultimate sudoku solver'))
        
        self.easy = Button(text='Easy (2x3)')
        self.add_widget(self.easy)
        self.medium = Button(text='Medium (3x3)')
        self.add_widget(self.medium)
        self.medium.bind(on_press=self.ThreeThree_button)
        self.hard1 = Button(text='Hard1 (3x4)')
        self.add_widget(self.hard1)
        self.hard2 = Button(text='Hard2 (4x3)')
        self.add_widget(self.hard2)
        self.extreme = Button(text='Extreme (4x4)')
        self.add_widget(self.extreme)
    
    def ThreeThree_button(self, instance):
        info = f'Attempting to configure your grid...'
        PuzzleApp.info_page.update_info(info)
        PuzzleApp.screen_manager.current = 'Info'
        Clock.schedule_once(self.grid, 2)
    
    def grid(self, _):        
        PuzzleApp.create_grid()
        PuzzleApp.screen_manager.current = 'Grid'
        

class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign='center', valign='middle', font_size=30)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)
    def update_info(self, message):
        self.message.text = message
    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)

class GridPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 9                                           # This needs to be udpated for each grid
        self.add_widget(Label(text='Please input numbers'))     # Need to make this its own row at the top (i.e. 9 cell wide)
        
        self.first_cell = TextInput(multiline=False)            # Need to automate these so we have GridPage(n.of.cells), and it makes that number of cells
        self.add_widget(self.first_cell)

        self.second_cell = TextInput(multiline=False)           # when these complete, if empty, assume zero for my sudoku code, else take value
        self.add_widget(self.second_cell)

        self.third_cell = TextInput(multiline=False)
        self.add_widget(self.third_cell)

        self.fourth_cell = TextInput(multiline=False)
        self.add_widget(self.fourth_cell)

        self.fifth_cell = TextInput(multiline=False)
        self.add_widget(self.fifth_cell)

        self.sixth_cell = TextInput(multiline=False)
        self.add_widget(self.sixth_cell)

        self.seventh_cell = TextInput(multiline=False)
        self.add_widget(self.seventh_cell)

        self.eighth_cell = TextInput(multiline=False)
        self.add_widget(self.eighth_cell)

        self.ninth_cell = TextInput(multiline=False)
        self.add_widget(self.ninth_cell)
        
        self.tenth_cell = TextInput(multiline=False)
        self.add_widget(self.tenth_cell)

        self.eleventh_cell = TextInput(multiline=False)
        self.add_widget(self.eleventh_cell)
    
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
    