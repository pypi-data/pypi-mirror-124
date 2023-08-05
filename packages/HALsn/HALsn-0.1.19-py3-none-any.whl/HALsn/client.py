#! /usr/bin/python

from socketMaster import cltHardwareClient
from scheduler import Routine
import pandas

# 192.168.217.203      # SHARKNINJA
# 192.168.109.128      # HOME VM

rout = Routine(freq=1)

cli = cltHardwareClient('192.168.217.203', 5050)
#cli.req_hw_enable('en_input_pump')

def bfnc_1(*args):
    #msg = cli.req_hw_status('input_pump_status')
    #print(f'{rout.ext_timer()}: {msg}')

    frame = pandas.read_csv('~/HALsn/HALsn/examples/sample_data/BAY_4-09-13-2021_1100-Cycle1.csv')

    cli.send_msg(cli.node, frame)

    print(rout.ext_timer())

    if rout.ext_timer() >= 30.0:
        cli.disconnect()
        return True

def bfnc_2(*args):
    cli.send_msg(cli.node, 'A String Type Message')
    print(rout.ext_timer())
    if rout.ext_timer() >= 30.0:
        cli.disconnect()
        return True

if cli.node_id == '01':
    rout.add_break_functions(bfnc_1, None)
if cli.node_id == '02':
    rout.add_break_functions(bfnc_2, None)
rout.run()
