#! /usr/bin/env python

from socketMaster import cltHardwareServer

# 192.168.217.203      # SHARKNINJA
# 192.168.109.128      # HOME VM

ser = cltHardwareServer('192.168.217.203', 5050)
ser.start()
