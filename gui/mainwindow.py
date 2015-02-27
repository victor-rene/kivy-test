#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: noseparser.pyx
# cython: profile=False

import codecs
import locale
import os
import shlex
import subprocess
os_encoding = locale.getpreferredencoding()
from itertools import islice
# from ctypes import cdll
# os_encoding = 'cp' + str(cdll.kernel32.GetACP())
# print os_encoding

from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from input.noseparser import NoseParser
from gui.loaddialog import LoadDialog
from gui.reportcell import ReportCell

    
class MainWindow(RelativeLayout):
    
    def __init__(self, **kwargs):
        self._initialized = False
        super(MainWindow, self).__init__(**kwargs)
        self.build_layout()
        self._initialized = True
        
    def build_layout(self):
        self.sv_left = ScrollView(size_hint=(None, None), pos_hint={'x': .0, 'y': .3})
        # self.sv_right = ScrollView(size_hint=(None, None), pos_hint={'x': .5, 'y': .3})
        self.tbl_cover = GridLayout(size_hint=(.5, .7), pos_hint={'x': .5, 'y': .3}, cols=1)
        self.tbl_cover.bind(on_touch_move=self.do_scroll)
        self.tbl_cover.orientation = 'tb-lr'
        # self.tbl_cover.bind(minimum_height=self.tbl_cover.setter('height'))
        self.treeview = TreeView(size_hint=(1., None))
        self.treeview.bind(minimum_height=self.treeview.setter('height'))
        self.console_in = TextInput(size_hint=(.7, .05), pos_hint={'x': .0, 'y': .25})
        self.console_in1 = TextInput(size_hint=(.7, .05), pos_hint={'x': .0, 'y': .2})
        self.console_out = TextInput(size_hint=(.7, .2), pos_hint={'x': .0, 'y': .0})
        self.console_in.multiline = False
        if os.path.isfile('cmd_in.txt'):
            with open('cmd_in.txt') as f:
                self.console_in.text = f.readline()
                self.console_in1.text = f.readline()
        self.console_out.multiline = True
        self.console_out.readonly = True
        self.sv_left.add_widget(self.treeview)
        self.add_widget(self.tbl_cover)
        self.add_widget(self.sv_left)
        # self.add_widget(self.sv_right)
        self.add_widget(self.console_in)
        self.add_widget(self.console_in1)
        self.add_widget(self.console_out)
        self.btn_run = Button(size_hint=(.3, .05), pos_hint={'x': .7, 'y': .25})
        self.btn_run.text = 'Run all'
        self.btn_run.bind(on_release=self.run)
        self.btn_run_one = Button(size_hint=(.3, .05), pos_hint={'x': .7, 'y': .2})
        self.btn_run_one.text = 'Run one'
        self.btn_run_one.bind(on_release=self.run_one)
        self.btn_load = Button(size_hint=(.3, .1), pos_hint={'x': .7, 'y': .1})
        self.btn_load.text = 'Load'
        self.btn_load.bind(on_release=self.load)
        self.btn_save = Button(size_hint=(.3, .1), pos_hint={'x': .7, 'y': .0})
        self.btn_save.text = 'Save'
        self.btn_save.bind(on_release=self.save)
        self.add_widget(self.btn_run)
        self.add_widget(self.btn_run_one)
        self.add_widget(self.btn_load)
        self.add_widget(self.btn_save)
        self.data = None
        self.parser = NoseParser()
        
    def on_size(self, *args):
        if self._initialized:
            sv_left_size = self.size[0] * .5, self.size[1] * .7
            self.sv_left.size = sv_left_size
            # sv_right_size = self.size[0] * .5, self.size[1] * .7
            # self.sv_right.size = sv_right_size
        
    def load(self, *args):
        ld = LoadDialog()
        ld.bind(on_dismiss=self.after_load)
        ld.open()
        
    def after_load(self, *args):
        ld = args[0]
        if ld.dialog_result:
            with open(ld.filename) as f:
                self.data = f.read()
                self.lines = self.data.split('\n')
                self.clear_tree()
                self.build_tree()
                self.build_cover()
                
    def clear_tree(self):
        for node in self.treeview.root.nodes:
            self.treeview.remove_node(node)
                
    def build_tree(self):
        if self.parser:
            lines = self.lines
            self.parser.parse_lines(lines)
            ref_list = []
            for k, v in self.parser.refs.iteritems():
                branch = TreeViewLabel(text=k+' ', markup=True)
                self.treeview.add_node(branch)
                for text in v:
                    self.treeview.add_node(TreeViewLabel(text=text, markup=True), branch)
                    if ']nok[' in text:
                        branch.text = branch.text + '[color=#ff0000]*[/color]'
                    # else: branch.text = branch.text + '[color=#00ff00]O[/color]'
                
    def build_cover(self):
        lines = self.lines
        n_lines = len(lines)
        tbl_limits = []
        for i in range(n_lines-1, 0, -1):
            line = lines[i]
            if line.startswith('-----'):
                tbl_limits.append(i)
            if len(tbl_limits) == 3:
                break
        lines_pct = [lines[i] for i in range(tbl_limits[2]+1, tbl_limits[1])]
        lines_data = []
        for line_pct in lines_pct:
            line_data = line_pct.split()
            line_data = '|'.join(line_data[:4])
            lines_data.append(line_data)
        self.build_tbl_cover(lines_data)
        
    def sort_by_pct(self, lines_data):
        """
        Data format is name, statements, misses, coverage percentage as string
        with separator '|'.
        """
        index = []
        for line_data in lines_data:
            l = line_data.split('|')
            index.append((int(l[3][:-1]), l))
        index.sort()
        return [d[1] for d in index]
        
    def build_tbl_cover(self, lines_data):
        self.tbl_cover.clear_widgets()
        # print lines_data
        lines_data = self.sort_by_pct(lines_data)
        for line_data in lines_data:
            self.tbl_cover.add_widget(ReportCell(data=line_data))
        self.offset = .05 * len(lines_data)
        self.tbl_cover.size_hint_y = self.offset
        self.tbl_cover.pos_hint = {'x': self.tbl_cover.pos_hint['x'],
                'y': 1. - self.offset}
        # self.tbl_cover.do_layout()
        
    def do_scroll(self, wgt, touch):
        # Recevies on_touch_move
        if wgt.collide_point(touch.x, touch.y):
            ry = (touch.dy / self.height) + self.tbl_cover.pos_hint['y']
            if ry > .3:
                ry = .3
            if ry <  1. - self.offset:
                ry =  1. - self.offset
            self.tbl_cover.pos_hint = {'x': .5, 'y': ry }
        # if self.tbl_cover.pos_hint
        # self.tbl_cover.do_layout()

    def run(self, *args):
        if self.console_in.text:
            try:
                cmd = shlex.split(self.console_in.text)
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
            
    def run_one(self, *args):
        if self.console_in1.text:
            try:
                cmd = shlex.split(self.console_in1.text)
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
        