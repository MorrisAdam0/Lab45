import sys
import time

from potentiostat import Potentiostat

from note_2 import PotentiostatLivePlot
dev = PotentiostatLivePlot(port='/dev/ttyACM2')

import matplotlib.pyplot as plt
import os

os.system('usbrelay')

'''
###############################################################################
Please alter the port and voltage range accordingly to the cyclic voltametry
test.
If NOT running a cyclic voltametry test, please IGNORE
###############################################################################
'''

pstat = Potentiostat('/dev/ttyACM2')

'''
###############################################################################
'''

def set_volt(i):
    voltage = pstat.set_volt(i); #In the TEST.py script put the voltage required in the brackets
    sys.stdout.write(str(voltage) + '\n')
    
    
    
def read_I():
    current = pstat.get_curr()
    sys.stdout.write(str(current) + '\n')

def valve_open_sequence(valve_no):
    x = int(valve_no)
    os.system('usbrelay')
    if x == 1:
        os.system('usbrelay 6QMBS_1=1')
    elif x == 2:
        os.system('usbrelay 6QMBS_2=1')
    elif x == 3:
        os.system('usbrelay 6QMBS_3=1')
    elif x == 4:
        os.system('usbrelay 6QMBS_4=1')
    elif x == 5:
        os.system('usbrelay 6QMBS_5=1')
    elif x == 6:
        os.system('usbrelay 6QMBS_6=1')
    elif x == 7:
        os.system('usbrelay 6QMBS_7=1')
    elif x == 8:
        os.system('usbrelay 6QMBS_8=1')
    
        
def valve_close_sequence(valve_no):
    x = int(valve_no)
    if x == 1:
        os.system('usbrelay 6QMBS_1=0')
    if x == 2:
        os.system('usbrelay 6QMBS_2=0')
    if x == 3:
        os.system('usbrelay 6QMBS_3=0')
    if x == 4:
        os.system('usbrelay 6QMBS_4=0')
    if x == 5:
        os.system('usbrelay 6QMBS_5=0')
    if x == 6:
        os.system('usbrelay 6QMBS_6=0')
    if x == 7:
        os.system('usbrelay 6QMBS_7=0')
    if x == 8:
        os.system('usbrelay 6QMBS_8=0')
    
