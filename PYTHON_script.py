from potentiostat import Potentiostat
import os
import sys
import time
import csv
import threading
import datetime


class Test():
    def __init__(self, pstat_path):
        self.pstat_path = pstat_path
        self.current_open_valve = 3
        self.solution = None
        self.pstat = Potentiostat(pstat_path)


    def open_valve(self, valve_number):
        self.current_open_valve = valve_number

        x = int(valve_number)
        os.system('usbrelay')
        if x == 1:
            os.system('usbrelay 6QMBS_1=1')
            self.solution = 'Sulfur'
        elif x == 2:
            os.system('usbrelay 6QMBS_2=1')
            self.solution = 'Deionized water'
        elif x == 3:
            os.system('usbrelay 6QMBS_3=1')
            self.solution = 'Deionized water'
        elif x == 4:
            os.system('usbrelay 6QMBS_4=1')
            self.solution = 'Deionized water'
        elif x == 5:
            os.system('usbrelay 6QMBS_5=1')
            self.solution = 'Deionized water'
        elif x == 6:
            os.system('usbrelay 6QMBS_6=1')
            self.solution = 'Cadmium'
        elif x == 7:
            os.system('usbrelay 6QMBS_7=1')
            self.solution = 'Ammmonia Buffer'
        elif x == 8:
            os.system('usbrelay 6QMBS_8=1')
            self.solution = 'Ammmonia Buffer'

    def close_valve(self, valve_number):
        x = int(valve_number)
        os.system('usbrelay')
        if x == 1:
            os.system('usbrelay 6QMBS_1=0')
        elif x == 2:
            os.system('usbrelay 6QMBS_2=0')
        elif x == 3:
            os.system('usbrelay 6QMBS_3=0')
        elif x == 4:
            os.system('usbrelay 6QMBS_4=0')
        elif x == 5:
            os.system('usbrelay 6QMBS_5=0')
        elif x == 6:
            os.system('usbrelay 6QMBS_6=0')
        elif x == 7:
            os.system('usbrelay 6QMBS_7=0')
        elif x == 8:
            os.system('usbrelay 6QMBS_8=0')

    def load(self, valve_number, time_valve_open, time_till_next_action):
        self.open_valve(valve_number)
        time.sleep(time_valve_open)
        self.close_valve(valve_number)
        time.sleep(time_till_next_action)

    def get_current_valve(self):
        return self.current_open_valve

    def get_current_solution(self):
        return self.solution

    def get_current_time(self):
        self.now = datetime.datetime.now().strftime("%H:%M:%S:%f")
        self.now = str(self.now)
        return self.now

    def read_current(self):
        current = self.pstat.get_curr()
        sys.stdout.write(str(current) + '\n')

    def read_voltage(self):
        voltage = self.pstat.get_volt()
        sys.stdout.write(str(voltage) + '\n')

    def setting_voltage(self, voltage):
        self.pstat.set_volt(voltage)
        sys.stdout.write(str(voltage) + '\n')

    def setting_current(self, current):
        self.pstat.set_curr(current)
        sys.stdout.write(str(current) + '\n')

    def CV(self, min_volt, max_volt, base_volt, number_cycles, volt_per_second):
        for i in range(number_cycles):
            datafile = 'data.txt'  # Output file for time, curr, volt data

            test_name = 'cyclic'  # The name of the test to run
            curr_range = '100uA'  # The name of the current range [-100uA, +100uA]
            sample_rate = 100.0  # The number of samples/second to collect
            volt_per_sec = volt_per_second  # Rate of transition from volt_min to volt_max (V/s)

            num_cycles = number_cycles  # The number of cycles in the waveform

            # Convert parameters to amplitude, offset, period, phase shift for triangle waveform
            amplitude = (max_volt - min_volt) / 2.0  # Waveform peak amplitude (V)
            offset = (max_volt + min_volt) / 2.0  # Waveform offset (V)
            period_ms = abs(int(1000 * 4 * amplitude / volt_per_sec))  # Waveform period in (ms)
            shift = 0.0  # Waveform phase shift - expressed as [0,1] number
            # 0 = no phase shift, 0.5 = 180 deg phase shift, etc.

            # Create dictionary of waveform parameters for cyclic voltammetry test
            test_param = {
                'quietValue': base_volt,
                'quietTime': 0,
                'amplitude': amplitude,
                'offset': offset,
                'period': period_ms,
                'numCycles': number_cycles,
                'shift': shift,
            }

            # Create potentiostat object and set current range, sample rate and test parameters

            self.pstat.set_curr_range(curr_range)
            self.pstat.set_sample_rate(sample_rate)
            self.pstat.set_param(test_name, test_param)

            # Run cyclic voltammetry test
            t, volt, curr = self.pstat.run_test(test_name, display='pbar', filename=datafile)

            os.system('cp 20221013.dat scratch.dat')
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

    def LSV(self, min_volt, max_volt, base_volt, number_cycles, volt_per_second):
        for i in range(number_cycles):
            datafile = 'data.txt'  # Output file for time, curr, volt data

            test_name = 'linearSweep'  # The name of the test to run
            curr_range = '100uA'  # The name of the current range [-100uA, +100uA]
            sample_rate = 100.0  # The number of samples/second to collect
            volt_per_sec = volt_per_second  # Rate of transition from volt_min to volt_max (V/s)

            num_cycles = number_cycles  # The number of cycles in the waveform

            # Convert parameters to amplitude, offset, period, phase shift for triangle waveform
            amplitude = (max_volt - min_volt) / 2.0  # Waveform peak amplitude (V)
            offset = (max_volt + min_volt) / 2.0  # Waveform offset (V)
            period_ms = abs(int(1000 * 4 * amplitude / volt_per_sec))  # Waveform period in (ms)
            shift = 0.0  # Waveform phase shift - expressed as [0,1] number
            # 0 = no phase shift, 0.5 = 180 deg phase shift, etc.

            # Create dictionary of waveform parameters for linear sweep voltammetry test
            test_param = {
                'quietTime': 0,  # quiet period voltage (V)
                'quietValue': base_volt,  # quiet period duration (ms)
                'startValue': min_volt,  # linear sweep starting value (V)
                'finalValue': max_volt,  # linear sweep final value (V)
                'duration': abs(int((max_volt - min_volt) / volt_per_sec)) * 1000
            }

            # Create potentiostat object and set current range, sample rate and test parameters
            # dev = Potentiostat(pstat)
            self.pstat.set_curr_range(curr_range)
            self.pstat.set_sample_rate(sample_rate)
            self.pstat.set_param(test_name, test_param)

            # Run linear voltammetry test
            t, volt, curr = self.pstat.run_test(test_name, display='pbar', filename=datafile)

            os.system('cp 20221013.dat scratch.dat')
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

def run_test(test: Test):
    """Run a test on the potentiostat"""
    for i in range(10):
        test.load(8, 10, 1)  # Turning Valve 8 on and putting buffer in the cell for 10 seconds with a 1 second wait

        test.setting_voltage(0.55)  # setting the voltage to 0.55
        test.load(1, 10, 1)  # Turning Valve 1 on and putting Sulfur in the cell for 10 seconds with a 1 second wait
        time.sleep(60)

        test.load(7, 10, 1)  # Turning Valve 7 on and putting buffer in the cell for 10 seconds with a 1 second wait

        test.setting_voltage(-0.75)  # setting the voltage to -0.75
        test.load(6, 10, 1)  # Turning Valve 6 on and putting Cadmium in the cell for 10 seconds with a 1 second wait
        time.sleep(60)

    test.load(8, 10, 1)  # Turning Valve 8 on and putting buffer in the cell for 10 seconds with a 1 second wait

    test.setting_voltage(0.55)  # setting the voltage to 0.55
    test.load(1, 10, 1)  # Turning Valve 1 on and putting Sulfur in the cell for 10 seconds with a 1 second wait
    time.sleep(60)

    test.load(7, 10, 1)  # Turning Valve 8 on and putting buffer in the cell for 10 seconds with a 1 second wait

def collect_data(test: Test):


    def creating_csv():
        with open('/home/i07lab45/Desktop/EC_howto/current_data.csv', mode='w') as current_data_csv:
            current_write = csv.writer(current_data_csv, delimiter=',')
            current_write.writerow(['Time (H:M:S:mS)', 'Voltage (V)', 'Current (I/uA)', 'Solution'])


    def write_to_csv():
        with open('/home/i07lab45/Desktop/EC_howto/current_data.csv', mode='a') as current_data:
            current_write = csv.writer(current_data, delimiter=',')
            write_to_log = current_write.writerow([test.get_current_time(), test.read_current(), test.read_voltage(), test.get_current_solution()])
            return write_to_log

    creating_csv()
    while True:
        try:
            write_to_csv()
            time.sleep(1)  # Needs to be modified - defines how many measurements you take per second
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    test = Test('/dev/ttyACM4')
    collect_data_thread = threading.Thread(target = lambda: collect_data(test), daemon = True)
    collect_data_thread.start()


    run_test(test)
