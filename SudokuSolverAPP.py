#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 17:13:06 2020

@author: dewiballard
"""
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
import re
import cv2
import os
import numpy as np
import pytesseract

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
        
        global listed_out
        listed_out = (np.zeros((n_cols, n_cols), dtype=np.uint8)).flatten()
        
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
            self.cells = FloatInput(multiline=False, font_size=35)
            self.add_widget(self.cells)
            a = str('cell'+str(i+1))
            my_dict[a] = self.cells
        
        self.image_it = Button(text='Take image', size_hint = (1, 2))
        self.add_widget(self.image_it)
        self.image_it.bind(on_press=self.Camera_button) 
        
        for i in range(number_of_columns-2):
            self.name = Label(text='')
            self.add_widget(self.name)
        
        self.solve_it = Button(text='Solve it', size_hint = (1, 2))
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


class GridPageTwo(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        number_of_columns = n_cols
        number_of_cells = n_cells
        self.cols = number_of_columns
        
        global my_dict
        my_dict = {}
        for i in range(number_of_cells):
            print(listed_out[i])
            if int(listed_out[i]) != 0:
                self.cells = FloatInput(text = str(listed_out[i]), multiline=False, font_size=35)
                self.add_widget(self.cells)
                a = str('cell'+str(i+1))
                my_dict[a] = self.cells
            else:
                self.cells = FloatInput(multiline=False, font_size=35)
                self.add_widget(self.cells)
                a = str('cell'+str(i+1))
                my_dict[a] = self.cells

        self.image_it = Button(text='Take image', size_hint = (1, 2))
        self.add_widget(self.image_it)
        self.image_it.bind(on_press=self.Camera_button) 
        
        for i in range(number_of_columns-2):
            self.name = Label(text='')
            self.add_widget(self.name)
        
        self.solve_it = Button(text='Solve it', size_hint = (1, 2))
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
        img = cv2.imread("puzzle_img.png")
        os.remove("puzzle_img.png")
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_clean = cv2.GaussianBlur(img_gray, (5, 5), 0)
        img_resize = cv2.resize(img_clean, (1080, 1080))
        global thresh
        ret, thresh = cv2.threshold(img_resize, 5, 255, cv2.THRESH_OTSU)
        cv2.imwrite("./output_image.png", thresh)
        PuzzleApp.corner_window()
        PuzzleApp.screen_manager.current = 'Corner Selector'

class CornerPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        size = Window.size
        self.img = Image(source ='output_image.png', keep_ratio=False, allow_stretch=True) 
        self.add_widget(self.img)
        self.use_img = Button(text='Use image', size_hint = (0.2, 0.1))
        self.use_img.pos = (size[0]*0.8, size[1]*0.05)
        self.add_widget(self.use_img)
        self.use_img.bind(on_press=self.read_image)
        self.topleft = Image(source ='red_circle.png', size_hint = (0.02, 0.02))
        self.topleft.pos = (size[0]*0.2, size[1]*0.8)
        self.add_widget(self.topleft)
        self.topright = Image(source ='red_circle.png', size_hint = (0.02, 0.02)) 
        self.topright.pos = (size[0]*0.8, size[1]*0.8)
        self.add_widget(self.topright)
        self.bottomleft = Image(source ='red_circle.png', size_hint = (0.02, 0.02)) 
        self.bottomleft.pos = (size[0]*0.2, size[1]*0.2)
        self.add_widget(self.bottomleft)
        self.bottomright = Image(source ='red_circle.png', size_hint = (0.02, 0.02)) 
        self.bottomright.pos = (size[0]*0.8, size[1]*0.2)
        self.add_widget(self.bottomright)

    def on_touch_move(self,touch):
        t_x,t_y = touch.pos
        tl_x,tl_y = self.topleft.pos
        tr_x,tr_y = self.topright.pos
        bl_x,bl_y = self.bottomleft.pos
        br_x,br_y = self.bottomright.pos
        if tl_x-100 < t_x < tl_x+100 and tl_y-100 < t_y < tl_y+100:
            self.topleft.pos = (t_x, t_y)
        if tr_x-100 < t_x < tr_x+100 and tr_y-100 < t_y < tr_y+100:
            self.topright.pos = (t_x, t_y)
        if bl_x-100 < t_x < bl_x+100 and bl_y-100 < t_y < bl_y+100:
            self.bottomleft.pos = (t_x, t_y)
        if br_x-100 < t_x < br_x+100 and br_y-100 < t_y < br_y+100:
            self.bottomright.pos = (t_x, t_y)
            
    def read_image(self, instance):
        size = Window.size
        top_left_coords = 1080*self.topleft.pos[0]/size[0], 1080 - 1080*self.topleft.pos[1]/size[1]
        top_right_coords = 1080*self.topright.pos[0]/size[0], 1080 - 1080*self.topright.pos[1]/size[1]
        bottom_left_coords = 1080*self.bottomleft.pos[0]/size[0], 1080 - 1080*self.bottomleft.pos[1]/size[1]      
        bottom_right_coords = 1080*self.bottomright.pos[0]/size[0], 1080 - 1080*self.bottomright.pos[1]/size[1]
        
        src = np.float32([top_left_coords,
                  top_right_coords,
                  bottom_left_coords,
                  bottom_right_coords])

        dst = np.float32([(0, 0),
                  (1080, 0),
                  (0, 1080),
                  (1080, 1080)])
    
        self.unwarp(thresh, src, dst, True)
    
    def unwarp(self, img, src, dst, testing):
        h, w = img.shape[:2]
        # use cv2.getPerspectiveTransform() to get M, the transform matrix
        M = cv2.getPerspectiveTransform(src, dst)
        # use cv2.warpPerspective() to warp image to correct angle
        warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)
        slicer = int(1080/n_cols)
        margin = int((1080/n_cols)*0.083)
        out = np.zeros((n_cols, n_cols), dtype=np.uint8)
        for x in range(n_cols):
            for y in range(n_cols):
                num = pytesseract.image_to_string(warped[margin + x*slicer:(x+1)*slicer - margin, margin + y*slicer:(y+1)*slicer - margin], lang ='eng', config='--psm 8 --oem 1 -c tessedit_char_whitelist=0123456789')
                if num:
                    out[x, y] = num
        print(out)
        global listed_out; listed_out = list(out.flatten())
        Clock.schedule_once(self.grid_two, 0.5)

    def grid_two(self, _):        
        PuzzleApp.create_grid_two()
        PuzzleApp.screen_manager.current = 'GridTwo'
        
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
    
    def create_grid_two(self):
        self.grid_page_two = GridPageTwo()
        screen = Screen(name='GridTwo')
        screen.add_widget(self.grid_page_two)
        self.screen_manager.add_widget(screen) 

    def camera_window(self):
        self.camera_page = CameraPage()
        screen = Screen(name='Camera')
        screen.add_widget(self.camera_page)
        self.screen_manager.add_widget(screen) 
        
    def corner_window(self):
        self.corner_page = CornerPage()
        screen = Screen(name='Corner Selector')
        screen.add_widget(self.corner_page)
        self.screen_manager.add_widget(screen) 
        
    def results_grid(self):
        self.results_page = ResultsPage()
        screen = Screen(name='Results')
        screen.add_widget(self.results_page)
        self.screen_manager.add_widget(screen) 
    
if __name__ == '__main__':
    PuzzleApp = SudokuSolverApp()
    PuzzleApp.run()
    