#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: main.py
# cython: profile=False

from kivy.app import App
from kivy.base import runTouchApp
from kivy.config import Config

# Config.set('kivy', 'window_icon', 'appicon.png')
Config.set('graphics', 'width', 1200)
Config.set('graphics', 'height', 900)

from gui.mainwindow import MainWindow

def resized(*args):
    print 'resized'

class MyApp(App):
    
    def build(self):
        from kivy.core.window import Window
        mw = MainWindow()
        Window.bind(on_resize=resized)
        return(mw)


if __name__ == '__main__':
    MyApp().run()
    # runTouchApp(MainWindow())
