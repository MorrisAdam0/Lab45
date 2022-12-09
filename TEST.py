'''
##############################################################################
        E_ALD Automated process script for sulfur and cadmium
        
        PLEASE change accordingly depending on the number of CV
            tests you wish to carry out and rest duration
                            between processes
                            
              Voltages are applied in the script at bottom
                            
##############################################################################
'''
import sys
import time

from potentiostat import Potentiostat

from note_2 import PotentiostatLivePlot
dev = PotentiostatLivePlot(port='/dev/ttyACM2')


import serial
import matplotlib.pyplot as plt
import os

import Test_kit as ts


pstat = ('/dev/ttyACM2')

'''
Valves and associated chemicals:
    1 - Sulfur
    2 - H2O
    3 - H2O
    4 - H2O
    5 - Cadmium
    6 - H2O
    7 - H2O
    8 - Buffer
'''

def read():
    ts.read_I()

def valve_open(valve_no):
    ts.valve_open_sequence(valve_no)
    
def valve_close(valve_no):
    ts.valve_close_sequence(valve_no)
    

def load(valve_no,time_valve_open, time_until_next_action):
    ts.valve_open_sequence(valve_no)
    time.sleep(time_valve_open)
    ts.valve_close_sequence(valve_no)
    time.sleep(time_until_next_action)
    


def setting_V(i):
    ts.set_volt(i)
    ts.read_I()
    time.sleep(2)

    
def CV(min_volt, max_volt, base_volt, number_cycles, volt_per_second):
    for i in range(number_cycles):
    
        datafile = 'data.txt'       # Output file for time, curr, volt data

        test_name = 'cyclic'        # The name of the test to run
        curr_range = '100uA'        # The name of the current range [-100uA, +100uA]
        sample_rate = 100.0         # The number of samples/second to collect
        volt_per_sec = volt_per_second #Rate of transition from volt_min to volt_max (V/s)
        
       
        num_cycles = number_cycles # The number of cycles in the waveform

        # Convert parameters to amplitude, offset, period, phase shift for triangle waveform
        amplitude = (max_volt - min_volt)/2.0            # Waveform peak amplitude (V)
        offset = (max_volt + min_volt)/2.0               # Waveform offset (V)
        period_ms = abs(int(1000*4*amplitude/volt_per_sec))   # Waveform period in (ms)
        shift = 0.0                                      # Waveform phase shift - expressed as [0,1] number
                                                         # 0 = no phase shift, 0.5 = 180 deg phase shift, etc.

        # Create dictionary of waveform parameters for cyclic voltammetry test
        test_param = {
                'quietValue' : base_volt,
                'quietTime'  : 0,
                'amplitude'  : amplitude,
                'offset'     : offset,
                'period'     : period_ms,
                'numCycles'  : number_cycles,
                'shift'      : shift,
                }

        # Create potentiostat object and set current range, sample rate and test parameters
        #dev = Potentiostat(pstat)    
        dev.set_curr_range(curr_range)  
        dev.set_sample_rate(sample_rate)
        dev.set_param(test_name,test_param)

        # Run cyclic voltammetry test
        t,volt,curr = dev.run_test(test_name,display='pbar',filename=datafile)
                   
        os.system('cp 20221013.dat scratch.dat' )
        filenames = ['scratch.dat', 'data.txt']
        with open("20221013.dat", "w") as outfile:
            with open('scratch.dat') as infile:      
                outfile.write(infile.read())            
            with open('data.txt') as infile:
                 outfile.write("\n")
                 outfile.write("#S     2 \n")
                 outfile.write("#D     2 \n")
                 outfile.write("#N     3 \n")         
                 outfile.write("#L  Eapp/V     E/V     I/uA \n")        
                 outfile.write(infile.read())
             

def LSV(min_volt, max_volt, base_volt, number_cycles, volt_per_second):
    for i in range(number_cycles):
    
        datafile = 'data.txt'       # Output file for time, curr, volt data

        test_name = 'linearSweep'        # The name of the test to run
        curr_range = '100uA'        # The name of the current range [-100uA, +100uA]
        sample_rate = 100.0         # The number of samples/second to collect
        volt_per_sec = volt_per_second #Rate of transition from volt_min to volt_max (V/s)
        
       
        num_cycles = number_cycles # The number of cycles in the waveform

        # Convert parameters to amplitude, offset, period, phase shift for triangle waveform
        amplitude = (max_volt - min_volt)/2.0            # Waveform peak amplitude (V)
        offset = (max_volt + min_volt)/2.0               # Waveform offset (V)
        period_ms = abs(int(1000*4*amplitude/volt_per_sec))   # Waveform period in (ms)
        shift = 0.0                                      # Waveform phase shift - expressed as [0,1] number
                                                         # 0 = no phase shift, 0.5 = 180 deg phase shift, etc.

        # Create dictionary of waveform parameters for linear sweep voltammetry test
        test_param = {
            'quietTime'  : 0,   # quiet period voltage (V)
            'quietValue' :  base_volt,   # quiet period duration (ms)
            'startValue' : min_volt,   # linear sweep starting value (V)
            'finalValue' :  max_volt,   # linear sweep final value (V)
            'duration' : abs(int((max_volt - min_volt)/volt_per_sec))*1000
            }
        
        # Create potentiostat object and set current range, sample rate and test parameters
        #dev = Potentiostat(pstat)    
        dev.set_curr_range(curr_range)  
        dev.set_sample_rate(sample_rate)
        dev.set_param(test_name,test_param)

        # Run linear voltammetry test
        t,volt,curr = dev.run_test(test_name,display='pbar',filename=datafile)
                   
        os.system('cp 20221013.dat scratch.dat' )
        filenames = ['scratch.dat', 'data.txt']
        with open("20221013.dat", "w") as outfile:
            with open('scratch.dat') as infile:      
                outfile.write(infile.read())            
            with open('data.txt') as infile:
                 outfile.write("\n")
                 outfile.write("#S     2 \n")
                 outfile.write("#D     2 \n")
                 outfile.write("#N     3 \n")         
                 outfile.write("#L  Eapp/V     E/V     I/uA \n")        
                 outfile.write(infile.read())
