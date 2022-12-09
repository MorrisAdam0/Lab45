from potentiostat import Potentiostat

from time import sleep
import datetime
import csv
import TEST
pstat = Potentiostat('/dev/ttyACM4')


def get_volt():
    volt = pstat.get_volt()
    volt = str(volt)
    return volt
    
def get_curr():
    curr = pstat.get_curr()
    curr = str(curr)
    return curr
    
def time_now():
    now = datetime.datetime.now().strftime("%H:%M:%S:%f:%p")
    now = str(now)
    return now
    
def get_solution():
    from Test import solution
    return solution

def write_to_csv():
    with open('/home/i07lab45/Desktop/EC_howto/current_data.csv', mode = 'a') as current_data:
        current_write = csv.writer(current_data, delimiter = ',')
        write_to_log = current_write.writerow([time_now(), get_curr(), get_volt(), get_solution()])
        return write_to_log
        
while True:
    try:
        write_to_csv()
        sleep(1) #Needs to be modified - defines how many measurements you take per second
    except KeyboardInterrupt:
        break
