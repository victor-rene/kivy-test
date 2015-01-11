#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: noseparser.py
# cython: profile=True


class NoseParser(object):
    
    def __init__(self, text=None):
        self.text = text
        self.listeners = []
        self.refs = dict()
        if self.text:
            self.parse_lines(text.split('\n'))
            
    def __del__(self):
        del self.listeners[:]
        
    def clear():
        self.refs.clear()
        
    def parse_lines(self, lines):
        for line in lines:
            self.parse_line(line)
        
    def parse_line(self, line):
        if line.startswith('#'):
            if line.endswith('ok'):
                line = self.add_markup_ok(line)
            space = line.index(' ')
            id = line[:space]
            self.refs[id] = line[space:]
        else:
            pass
        self.notify('line_parsed')
    
    def add_markup_ok(self, line):
        return line[:-2] + '[color=#00ff00]ok[/color]'
        
    def notify(self, event_name, *args, **kwargs):
        for listener in self.listeners:
            if event_name in listener.events:
                getattr(listener, event_name)(*args, **kwargs)
