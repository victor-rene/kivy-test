#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: main.py
# cython: profile=False

from kivy.base import runTouchApp
from kivy.config import Config

Config.set('graphics', 'width', 1200)
Config.set('graphics', 'height', 900)

from gui.mainwindow import MainWindow


if __name__ == '__main__':
    runTouchApp(MainWindow())
