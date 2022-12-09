import TEST as cell
import Test_kit as tk
import time

for i in range(10):
    cell.load(8, 10, 1) #Turning Valve 8 on and putting buffer in the cell for 10 seconds with a 1 second wait
    
    cell.setting_V(0.55) #setting the voltage to 0.55
    cell.load(1, 10, 1) #Turning Valve 1 on and putting Sulfur in the cell for 10 seconds with a 1 second wait
    time.sleep(60) 
    
    cell.load(7, 10, 1)#Turning Valve 7 on and putting buffer in the cell for 10 seconds with a 1 second wait
    
    cell.setting_V(-0.75)#setting the voltage to -0.75
    cell.load(6, 10, 1)#Turning Valve 6 on and putting Cadmium in the cell for 10 seconds with a 1 second wait
    time.sleep(60)

cell.load(8, 10, 1) #Turning Valve 8 on and putting buffer in the cell for 10 seconds with a 1 second wait
    
cell.setting_V(0.55) #setting the voltage to 0.55
cell.load(1, 10, 1) #Turning Valve 1 on and putting Sulfur in the cell for 10 seconds with a 1 second wait
time.sleep(60)

cell.load(7, 10, 1) #Turning Valve 8 on and putting buffer in the cell for 10 seconds with a 1 second wait
