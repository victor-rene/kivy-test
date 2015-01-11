#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: noseparser.pyx
# cython: profile=False

import codecs
# import io
import locale
import os
import shlex
import subprocess
os_encoding = locale.getpreferredencoding()
# import sys
# from ctypes import cdll
# os_encoding = 'cp' + str(cdll.kernel32.GetACP())
# print os_encoding
# print os_encoding

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
        
    def build_layout(self):
        self.treeview = TreeView(size_hint=(.7, .7), pos_hint={'x': .0, 'y': .3})
        self.listview = ListView(size_hint=(.3, .7), pos_hint={'x': .7, 'y': .3})
        self.console_in = TextInput(size_hint=(.7, .1), pos_hint={'x': .0, 'y': .2})
        self.console_out = TextInput(size_hint=(.7, .2), pos_hint={'x': .0, 'y': .0})
        self.console_in.multiline = False
        if os.path.isfile('cmd_in.txt'):
            with open('cmd_in.txt') as f:
                self.console_in.text = f.readline() # Read only first line
        self.console_out.multiline = True
        self.console_out.readonly = True
        self.add_widget(self.treeview)
        self.add_widget(self.listview)
        self.add_widget(self.console_in)
        self.add_widget(self.console_out)
        self.btn_run = Button(size_hint=(.3, .1), pos_hint={'x': .7, 'y': .2})
        self.btn_run.text = 'Run'
        self.btn_run.bind(on_release=self.run)
        self.add_widget(self.btn_run)
        self.btn_load = Button(size_hint=(.3, .1), pos_hint={'x': .7, 'y': .1})
        self.btn_load.text = 'Load'
        self.btn_load.bind(on_release=self.load)
        self.add_widget(self.btn_load)
        self.btn_save = Button(size_hint=(.3, .1), pos_hint={'x': .7, 'y': .0})
        self.btn_save.text = 'Save'
        self.btn_save.bind(on_release=self.save)
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
            ref_list = []
            for k, v in self.parser.refs.iteritems():
                ref = k + ': ' + v
                ref_list.append(ref)
            ref_list.sort()
            for ref in ref_list:
                self.treeview.add_node(TreeViewLabel(text=ref, markup=True))

    def run(self, *args):
        if self.console_in.text:
            try:
                cmd = shlex.split(self.console_in.text)
                # out = codecs.open('%s.txt' % encoding, 'w', encoding)
    # out.write('# coding = %s\n' % encoding)
    # out.write(u'\u201chello se\u00f1nor\u201d')
    # out.close()
                # with open('cmd_output.txt', 'w') as fw:
                # stdout = io.open(p.stdout.fileno(), encoding='utf-8')
                with codecs.open('cmd_out.txt', 'w', os_encoding) as fw:
                    p = subprocess.Popen(cmd, stdout=fw, stderr=fw, shell=True)
                    p.wait()
                with codecs.open('cmd_out.txt', 'r', os_encoding) as fr:
                    self.console_out.text = fr.read()
            except Exception, e:
                import traceback
                print traceback.format_exc()
        else:
            self.console_out.text = 'ERROR: No command to execute.'
        
    def save(self, *args):
        pass
        