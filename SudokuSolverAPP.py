#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 17:13:06 2020

@author: dewiballard
"""
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import image_slicer
import time
import re

class PuzzleSelector(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
        self.add_widget(Label(text='Sudoku solver app'))
        
        self.easy = Button(text='Easy (2x3)')
        self.add_widget(self.easy)
        self.easy.bind(on_press=self.grid_size)
        self.easy.bind(on_press=self.Grid_button)
        
        self.medium = Button(text='Medium (3x3)')
        self.add_widget(self.medium)
        self.medium.bind(on_press=self.grid_size)
        self.medium.bind(on_press=self.Grid_button)
        
        self.hard = Button(text='Hard (3x4)')
        self.add_widget(self.hard)
        self.hard.bind(on_press=self.grid_size)
        self.hard.bind(on_press=self.Grid_button)
        
        self.extreme = Button(text='Extreme (4x4)')
        self.add_widget(self.extreme)
        self.extreme.bind(on_press=self.grid_size)
        self.extreme.bind(on_press=self.Grid_button)
        
        self.impossible = Button(text='Impossible (5x5)')
        self.add_widget(self.impossible)
        self.impossible.bind(on_press=self.grid_size)
        self.impossible.bind(on_press=self.Grid_button)
        
    def grid_size(self, instance):
        global n_cols
        global n_cells
        if instance.text == 'Easy (2x3)':
            n_cols = 6
            n_cells = 36
        if instance.text == 'Medium (3x3)':
            n_cols = 9
            n_cells = 81
        if instance.text == 'Hard (3x4)':
            n_cols = 12
            n_cells = 144
        if instance.text == 'Extreme (4x4)':
            n_cols = 16
            n_cells = 256
        if instance.text == 'Impossible (5x5)':
            n_cols = 25
            n_cells = 625
        
    def Grid_button(self, instance):
        info = f'Attempting to configure your grid, please enter your known values...'
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
        number_of_columns = n_cols
        number_of_cells = n_cells
        self.cols = number_of_columns
        
        global my_dict
        my_dict = {}
        for i in range(number_of_cells):
            self.cells = FloatInput(multiline=False, font_size=35)            #potentially ID this
            self.add_widget(self.cells)
            a = str('cell'+str(i+1))
            my_dict[a] = self.cells
   
        self.image_it = Button(text='Take image')
        self.add_widget(self.image_it)
        self.image_it.bind(on_press=self.Camera_button) 
        
        for i in range(number_of_columns-2):
            self.name = Label(text='')
            self.add_widget(self.name)
        
        self.solve_it = Button(text='Solve it')                                 # For next (solver part), assume 0 if empty...
        self.add_widget(self.solve_it)
        self.solve_it.bind(on_press=self.Results_button)
           
    def Camera_button(self, instance):
        notice = f'Opening camera'
        PuzzleApp.notice_page.update_info(notice)
        PuzzleApp.screen_manager.current = 'Notice'
        Clock.schedule_once(self.camera, 1.5)
        
    def camera(self, _):        
        PuzzleApp.camera_window()
        PuzzleApp.screen_manager.current = 'Camera'
        
    def Results_button(self, instance):
        message = f'Solving grid, please wait...'
        PuzzleApp.message_page.update_info(message)
        PuzzleApp.screen_manager.current = 'Message'
        global my_dict2
        my_dict2 = {}
        for item in my_dict:
            if my_dict[item].text == '':
                my_dict2[item] = 0
            else:
                my_dict2[item] = my_dict[item].text
        print(my_dict2)
        Clock.schedule_once(self.results, 3)
        
    def results(self, _):        
        PuzzleApp.results_grid()
        PuzzleApp.screen_manager.current = 'Results'

class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '[^0-9]' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '[^0-9]'.join([re.sub(pat, '', s) for s in substring.split('[^0-9]', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

class NoticePage(GridLayout):
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

Builder.load_string('''
<CameraPage>:
    orientation: 'vertical'
    Camera:
        size_hint: 1, 1
        id: camera
        resolution: (1280, 720)
        keep_ratio: False
        allow_stretch: True
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size_hint_y: 0.65
        size_hint_x: 1
        play: True
    ToggleButton:
        text: 'Take / Retake'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Use image'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')                                                                            #on_press: go to grid page, with the numbers read filled in...
    
class CameraPage(BoxLayout):
    def capture(self):
        camera = self.ids['camera']
        camera.export_to_png("puzzle_img.png")
        image_slicer.slice('puzzle_img.png', n_cells)

class MessagePage(GridLayout):
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
        
class ResultsPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        number_of_columns = n_cols
        number_of_cells = n_cells
        self.cols = number_of_columns
        
        for i in range(number_of_cells):
            self.name = Label(text='input', font_size = 35)
            self.add_widget(self.name)
        
class SudokuSolverApp(App):
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
        
        self.notice_page = NoticePage()
        screen = Screen(name='Notice')
        screen.add_widget(self.notice_page)
        self.screen_manager.add_widget(screen)
        
        self.message_page = MessagePage()
        screen = Screen(name='Message')
        screen.add_widget(self.message_page)
        self.screen_manager.add_widget(screen)
        
        return self.screen_manager

    def create_grid(self):
        self.grid_page = GridPage()
        screen = Screen(name='Grid')
        screen.add_widget(self.grid_page)
        self.screen_manager.add_widget(screen) 

    def camera_window(self):
        self.camera_page = CameraPage()
        screen = Screen(name='Camera')
        screen.add_widget(self.camera_page)
        self.screen_manager.add_widget(screen) 
        
    def results_grid(self):
        self.results_page = ResultsPage()
        screen = Screen(name='Results')
        screen.add_widget(self.results_page)
        self.screen_manager.add_widget(screen) 
    
if __name__ == '__main__':
    PuzzleApp = SudokuSolverApp()
    PuzzleApp.run()
    