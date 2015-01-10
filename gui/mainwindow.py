#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: noseparser.pyx
# cython: profile=False

import os
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.listview import ListView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from input.noseparser import NoseParser
from gui.loaddialog import LoadDialog

    
class MainWindow(RelativeLayout):
    
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.build_layout()
        self.cmd = 'nosetests '
        
    def build_layout(self):
        self.treeview = TreeView(size_hint=(.7, .7), pos_hint={'x': .0, 'y': .3})
        self.listview = ListView(size_hint=(.3, .7), pos_hint={'x': .7, 'y': .3})
        self.console = TextInput(size_hint=(.7, .3), pos_hint={'x': .0, 'y': .0})
        self.console.multiline = True
        self.btn_load = Button(size_hint=(.3, .1), pos_hint={'x': .7, 'y': .2})
        self.btn_load.text = 'Load'
        self.btn_load.bind(on_press=self.load)
        self.add_widget(self.btn_load)
        self.btn_run = Button(size_hint=(.3, .1), pos_hint={'x': .7, 'y': .1})
        self.btn_run.text = 'Run'
        self.btn_run.bind(on_press=self.run)
        self.add_widget(self.btn_run)
        self.btn_save = Button(size_hint=(.3, .1), pos_hint={'x': .7, 'y': .0})
        self.btn_save.text = 'Save'
        self.btn_save.bind(on_press=self.save)
        self.add_widget(self.btn_save)
        self.data = None
        self.parser = NoseParser()
        
    def load(self, *args):
        ld = LoadDialog()
        ld.bind(on_dismiss=self.after_load)
        ld.open()
        
    def after_load(self, *args):
        ld = args[0]
        if ld.dialog_result:
            with open(ld.filename) as f:
                self.data = f.read()
                self.call_parser()
                
    def call_parser(self):
        if self.parser:
            lines = self.data.split('\n')
            self.parser.parse_lines(lines)
            for k, v in self.parser.refs.iteritems():
                ref = k + ': ' + v
                self.treeview.add(TreeViewLabel(text=ref))

    def run(self, *args):
        pass
        
    def save(self, *args):
        pass
        