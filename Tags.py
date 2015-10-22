#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import signal
import GUI

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':
  sys.exit(GUI.app.exec_())