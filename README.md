# Lab45

The following is a record of the current Python scripts for running tests and analysing data from lab45.
Updated 20/04/23
# 2script.py
This is the test procedure script

All that is needed is to: 
  - Change the port location at the bottom of the script
  - Change the file name of the CV and LSV data locations
  - Change the name of the csv file recording [Time, Current, Voltage, Solution]
  
  
# Current_data_analysis_updated.py
Script should run fine as long as the current_data.csv file is in the same folder. if not copy it across or change the file location address
Similar to Pymca you can zoom in on sections of the graph and adjust view using the icons in the top right

![image](https://user-images.githubusercontent.com/115980966/206751684-d760d272-6d0f-453a-b280-cc90e7678bba.png)
![image](https://user-images.githubusercontent.com/115980966/206751718-db0508fd-f229-4241-8664-d00197cb0031.png)
![image](https://user-images.githubusercontent.com/115980966/206751733-87b7c14e-5796-4ef8-bc71-86eaa81102b0.png)


# Stripping_curve_integration.py
Steps for the calculation:
1. Change the filename to the directory location of the experimental test csv file.
2. Run the Script
3. From the graph that will load in the browser, enter the two x-coordinates for the line of best fit that defines the region you want to calculate
4. Calculation will proceed
5. Results will be inserted into the Electrochemical_stripping_data.csv file

![image](https://user-images.githubusercontent.com/115980966/235660593-dd57fa38-8922-4e02-8ac6-5483cda9de36.png)
![image](https://user-images.githubusercontent.com/115980966/235660819-e1eee024-5062-4268-889f-234bca8c62aa.png)
![image](https://user-images.githubusercontent.com/115980966/235661166-3cd32923-a1d2-40ce-8bf4-4082907f157d.png)


# Potentiostat GUI
Features:
- Toggle Electrode Status (ON and OFF)
- Select Current and Voltage Ranges
- Toggle the appearance of the GUI
- Write a script using buttons to insert commands with parameters inputed by the user
- Save the script, such that the file 2script.py can then be run, resulting in all data colelction occcuring as expected
- Run the script
- Can toggle a specific valve for a specific time via the 'Custom Valve Openeing' button
- Can manually toggle each valve ON and OFF, with a timer displaying the count of tme from the onset of the Open button
- The user can manually <Set the Voltage>, <Get Current>, <Get voltage>, <Get Current Range>, <Get Voltage Range>, <Turn Electrode Auto Connect OFF>, <Turn Electrodes OFF>, <Turn Electrodes ON>
- All ouputs of user entries are shown in the terminal


![image](https://github.com/MorrisAdam0/Lab45/assets/115980966/6fa156d1-f453-4298-8a67-1367d360e645)

