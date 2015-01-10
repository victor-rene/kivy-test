#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: main.py
# cython: profile=False

import os
from functools import partial

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView


class LoadDialog(Popup):
    
    def __init__(self, **kwargs):
        super(LoadDialog, self).__init__(**kwargs)
        self.title = "Load file..."
        self.size_hint = (0.9, 0.9)
        self.content = LoadDialogContent(self)
        self.dialog_result = None
        
    def load(self, directory, file_name, *args):
        """ Stores filename. """
        print directory, file_name
        if directory and file_name:
            filename = os.path.join(directory, file_name[0])
            if os.isfile(filename):
                self.filename = filename
                self.dialog_result = True
                print 'dr True'
        self.dismiss()


class LoadDialogContent(BoxLayout):
    
    def __init__(self, root, **kwargs):
        super(LoadDialogContent, self).__init__(**kwargs)
        self.root = root
        self.orientation = "vertical"
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        try:
            self.filechooser = FileChooserListView(path=curr_dir)
        except Exception, e:
            import traceback
            print traceback.format_exc()
        self.box_btn = BoxLayout(height=30, size_hint_y=None)
        self.btn_cancel = Button(text='Cancel')
        self.btn_cancel.bind(on_release=self.root.dismiss)
        self.btn_load = Button(text='Load')
        self.btn_load.bind(on_release=partial(self.root.load, 
                self.filechooser.path, self.filechooser.selection))
        self.box_btn.add_widget(self.btn_cancel)
        self.box_btn.add_widget(self.btn_load)
        self.add_widget(self.filechooser)
        self.add_widget(self.box_btn)

        
