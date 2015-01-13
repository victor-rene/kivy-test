#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: noseparser.py
# cython: profile=True

from node import Node
from collections import OrderedDict


class NoseParser(object):
    
    def __init__(self, text=None):
        self.text = text
        self.listeners = []
        self.refs = OrderedDict()
        if self.text:
            self.parse_lines(text.split('\n'))
            
    def __del__(self):
        del self.listeners[:]
        
    def clear():
        self.refs.clear()
        
    def parse_lines(self, lines):
        nl = []
        states = []
        state = None
        can_process_state = False
        for line in lines:
            if line.startswith('#'):
                can_process_state = True
                states.append(state)
                state = False
                n = Node()
                n.parse(line)
                nl.append((n.unit, n))
            if can_process_state:
                if not state: # processing the last state is tricky
                    state = line.endswith('ok')
                    can_process_state = False # used to create a bunch of false negative and screenshot
        states.append(state)
        del states[0]
        # print len(nl), nl
        # print len(states), states
        n_nodes = len(nl)
        for i in range(n_nodes):
            node = nl[i][1]
            state = states[i]
            s = ''
            if state:
                s = self.add_markup_ok(s)
            else: s = self.add_markup_nok(s)
            s += ' ' + self.add_markup_id(node.id) + ' ' + node.name
                
            if node.unit not in self.refs:
                self.refs[node.unit] = [s]
            else:
                self.refs[node.unit].append(s)
    
    def add_markup_ok(self, line):
        return '[color=#00ff00]ok[/color]'
        
    def add_markup_nok(self, line):
        return '[color=#ff0000]nok[/color]'
        
    def add_markup_id(self, id):
        return '[color=#ffff00]%s[/color]' % id
        
    # def notify(self, event_name, *args, **kwargs):
        # for listener in self.listeners:
            # if event_name in listener.events:
                # getattr(listener, event_name)(*args, **kwargs)
