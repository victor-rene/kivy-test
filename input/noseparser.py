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
        
    def parse_line(self):
        if line.startswith('#'):
            space = line.index(' ')
            id = line[:space]
            refs[id] = line
        else:
            pass
        self.notify('line_parsed')
        
    def notify(self, event_name, *args, **kwargs):
        for listener in self.listeners:
            if event_name in listener.events:
                getattr(listener, event_name)(*args, **kwargs)
