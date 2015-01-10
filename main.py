#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: main.py
# cython: profile=False

from kivy.base import runTouchApp

from gui.mainwindow import MainWindow


if __name__ == '__main__':
    runTouchApp(MainWindow())
