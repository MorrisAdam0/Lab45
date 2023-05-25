import tkinter as tk
from datetime import *
from datetime import datetime
from potentiostat import Potentiostat
import time
import sys
import io
import subprocess
import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Test:
    def __init__(self, pstat_path):
        self.pstat_path = pstat_path
        self.current_open_valve = 3
        self.solution = None
        self.pstat = Potentiostat(pstat_path)
        # self.pstat.set_volt_range('2V')
        self.test_finished = False

        self.pstat.set_auto_connect(False)


class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        #self.test = Test('COM3')

        self.title('Potentiostat GUI')
        self.geometry('800x600')

        # configure grid layout

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        #create sidebar with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, height=600, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text='Potentiostat GUI', font=ctk.CTkFont(size=20, weight='bold', underline=True))
        self.logo_label.grid(row=0, column=0, padx=20, pady=10)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text='Author: Adam Morris',font=ctk.CTkFont(size=10, weight='bold'))
        self.logo_label.grid(row=0, column=1, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self.sidebar_frame, text='Status: OFF', anchor='w', text_color='black', fg_color='red', corner_radius=10)
        self.status_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        #self.test.pstat.set_auto_connect(False)
        #self.test.pstat.set_all_elect_connected(False)
        #self.test.pstat.set_volt(-1)



        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text='Turn ON Potentiostat', command=self.turn_on_pstat)
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text='Turn OFF Potentiostat', command=self.turn_off_pstat)
        self.sidebar_button_2.grid(row=2, column=1, padx=20, pady=10)

        combox_var_1 = ctk.StringVar(value="Current Range")
        self.sidebar_combobox = ctk.CTkComboBox(self.sidebar_frame, values=["1uA", "10uA", "100uA", "1000uA"], variable=combox_var_1, command=self.set_current_range)
        self.sidebar_combobox.grid(row=3, column=0, padx=20, pady=10)

        combox_var_2 = ctk.StringVar(value="Voltage Range")
        self.sidebar_combobox_2 = ctk.CTkComboBox(self.sidebar_frame, values=["1V", "2V", "5V", "10V"], variable=combox_var_2, command=self.set_voltage_range)
        self.sidebar_combobox_2.grid(row=3, column=1, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame,
                                                             values=["Dark", "Light", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 10))
        #============================================================================================
        #============================================================================================
        #============================================================================================

        #TEXT FRAME

        self.text_frame = ctk.CTkFrame(self, corner_radius=0)
        self.text_frame.grid(row=0, column=1, padx=(20,20), pady=(20,0), sticky='nsew')

        self.logo_label = ctk.CTkLabel(self.text_frame, text='Script',
                                        font=ctk.CTkFont(size=20, weight='bold', underline=True))
        self.logo_label.grid(row=0, column=0, padx=20, pady=10)

        self.textbox = ctk.CTkTextbox(self.text_frame, width=400, height=400, corner_radius=10, text_color='white')
        self.textbox.grid(row=1, column=0, padx=20, pady=10)



        #===========
        #setting voltage button
        #===========
        def input_window_voltage():
            input_window = ctk.CTkToplevel(self)
            input_window.transient(self)
            input_window.title("Setting Voltage")


            # Function to handle the 'ok' button click
            def handle_ok():
                voltage = voltage_entry.get()
                self.textbox.insert("end", f"\ntest.setting_voltage({voltage})")

                input_window.destroy()

            #create a label for the valve number
            voltage_label = ctk.CTkLabel(input_window, text="Enter Voltage:")
            voltage_label.grid(row=0, column=0, padx=20, pady=10)
            voltage_entry = ctk.CTkEntry(input_window)
            voltage_entry.grid(row=1, column=0, padx=20, pady=10)

            ok_button = ctk.CTkButton(input_window, text="OK", command=handle_ok)
            ok_button.grid(row=4, column=0, padx=20, pady=10)

        # Creating a valve status label
        voltage_label = ctk.CTkButton(self.text_frame, text="Setting Voltage", command=input_window_voltage)
        voltage_label.grid(row=2, column=0, padx=20, pady=10)

        #===========
        #loading solution
        #===========
        def input_window_load():
            input_window = ctk.CTkToplevel(self)
            input_window.transient(self)
            input_window.title("Loading Solution")

            # Function to handle the 'ok' button click
            def handle_ok():
                valve_num = valve_num_entry.get()
                time = time_entry.get()
                time_until_next = time_until_next_entry.get()

                #validate
                if not valve_num.isdigit() or int(valve_num) not in range(1, 9):
                    messagebox.showerror("Invalid Input", "Valve number must be an integer between 1 and 8")
                    return
                if not time.isdigit():
                    messagebox.showerror("Invalid Input", "Time period value must be a non-negative integer")
                    return
                if not time_until_next.isdigit():
                    messagebox.showerror("Invalid Input", "Time until next must be a non-negative integer")
                    return
                # Display the sentenc ein the text widget
                self.textbox.insert("end", f"\ntest.load_solution({valve_num}, {time}, {time_until_next})")

                input_window.destroy()

            valve_num_label = ctk.CTkLabel(input_window, text="Enter Valve Number:")
            valve_num_label.grid(row=0, column=0, padx=20, pady=10)
            valve_num_entry = ctk.CTkEntry(input_window)
            valve_num_entry.grid(row=1, column=0, padx=20, pady=10)

            time_label = ctk.CTkLabel(input_window, text="Enter Time Period:")
            time_label.grid(row=2, column=0, padx=20, pady=10)
            time_entry = ctk.CTkEntry(input_window)
            time_entry.grid(row=3, column=0, padx=20, pady=10)

            time_until_next_label = ctk.CTkLabel(input_window, text="Enter Time Until Next Action:")
            time_until_next_label.grid(row=4, column=0, padx=20, pady=10)
            time_until_next_entry = ctk.CTkEntry(input_window)
            time_until_next_entry.grid(row=5, column=0, padx=20, pady=10)

            ok_button = ctk.CTkButton(input_window, text="OK", command=handle_ok)
            ok_button.grid(row=6, column=0, padx=20, pady=10)

        # creating a button to load solution
        load_solution_button = ctk.CTkButton(self.text_frame, text="Load Solution", command=input_window_load)
        load_solution_button.grid(row=2, column=1, padx=20, pady=10)

        #===========
        #SLEEP
        #===========

        def input_window_sleep():
            input_window = ctk.CTkToplevel(self)
            input_window.transient(self)
            input_window.title("Sleep")

            # Function to handle the 'ok' button click
            def handle_ok():
                sleep = sleep_entry.get()
                #validate
                if not sleep.isdigit():
                    messagebox.showerror("Invalid Input", "Sleep value must be a non-negative integer")
                    return

                # Display the sentenc ein the text widget
                self.textbox.insert("end", f"\nawait asyncio.sleep({sleep})")

                input_window.destroy()

            sleep_label = ctk.CTkLabel(input_window, text="Enter Sleep Value:")
            sleep_label.grid(row=0, column=0, padx=20, pady=10)
            sleep_entry = ctk.CTkEntry(input_window)
            sleep_entry.grid(row=1, column=0, padx=20, pady=10)

            ok_button = ctk.CTkButton(input_window, text="OK", command=handle_ok)
            ok_button.grid(row=2, column=0, padx=20, pady=10)

        # creating a button to sleep
        sleep_button = ctk.CTkButton(self.text_frame, text="Sleep", command=input_window_sleep)
        sleep_button.grid(row=3, column=0, padx=20, pady=10)

        #===========
        #CV
        #===========

        def input_window_cv():
            input_window = ctk.CTkToplevel(self)
            input_window.transient(self)
            input_window.title("CV")

            # Function to handle the 'ok' button click
            def handle_ok():
                from_volt = from_volt_entry.get()
                to_volt = to_volt_entry.get()

                #validate
                if not from_volt.isdigit():
                    messagebox.showerror("Invalid Input", "From voltage value must be a non-negative integer")
                    return
                if not to_volt.isdigit():
                    messagebox.showerror("Invalid Input", "To voltage value must be a non-negative integer")
                    return

                # Display the sentenc ein the text widget
                self.textbox.insert("end", f"\ntest.cv({from_volt}, {to_volt}, 1, 0.050)")

                input_window.destroy()

            from_volt_label = ctk.CTkLabel(input_window, text="Enter Start Voltage:")
            from_volt_label.grid(row=0, column=0, padx=20, pady=10)
            from_volt_entry = ctk.CTkEntry(input_window)
            from_volt_entry.grid(row=1, column=0, padx=20, pady=10)

            to_volt_label = ctk.CTkLabel(input_window, text="Enter 'Up to' Voltage:")
            to_volt_label.grid(row=2, column=0, padx=20, pady=10)
            to_volt_entry = ctk.CTkEntry(input_window)
            to_volt_entry.grid(row=3, column=0, padx=20, pady=10)

            ok_button = ctk.CTkButton(input_window, text="OK", command=handle_ok)
            ok_button.grid(row=4, column=0, padx=20, pady=10)

        # creating a button to cv
        cv_button = ctk.CTkButton(self.text_frame, text="CV", command=input_window_cv)
        cv_button.grid(row=3, column=1, padx=20, pady=10)

        #===========
        #LSV
        #===========

        def input_window_lsv():
            input_window = ctk.CTkToplevel(self)
            input_window.transient(self)
            input_window.title("LSV")

            # Function to handle the 'ok' button click
            def handle_ok():
                from_volt = from_volt_entry.get()
                to_volt = to_volt_entry.get()


                #validate
                if not from_volt.isdigit():
                    messagebox.showerror("Invalid Input", "From voltage value must be a non-negative integer")
                    return
                if not to_volt.isdigit():
                    messagebox.showerror("Invalid Input", "To voltage value must be a non-negative integer")
                    return

                # Display the sentenc ein the text widget
                self.textbox.insert("end", f"\ntest.LSV({from_volt}, {to_volt}, 1, 0.050)")

                input_window.destroy()

            from_volt_label = ctk.CTkLabel(input_window, text="Enter Start Voltage:")
            from_volt_label.grid(row=0, column=0, padx=20, pady=10)
            from_volt_entry = ctk.CTkEntry(input_window)
            from_volt_entry.grid(row=1, column=0, padx=20, pady=10)

            to_volt_label = ctk.CTkLabel(input_window, text="Enter End Voltage:")
            to_volt_label.grid(row=2, column=0, padx=20, pady=10)
            to_volt_entry = ctk.CTkEntry(input_window)
            to_volt_entry.grid(row=3, column=0, padx=20, pady=10)

            ok_button = ctk.CTkButton(input_window, text="OK", command=handle_ok)
            ok_button.grid(row=4, column=0, padx=20, pady=10)

        # creating a button to lsv
        lsv_button = ctk.CTkButton(self.text_frame, text="LSV", command=input_window_lsv)
        lsv_button.grid(row=3, column=2, padx=20, pady=10)

        #===========
        #SAVE
        #===========

        def save_script():
            script_content = self.textbox.get("1.0", "end-1c")
            #retrieve the content of the Text widget
            with open('user_script.py', 'w') as f:
                f.write(script_content)

        save_button = ctk.CTkButton(self.text_frame, text="Save Script", command=save_script)
        save_button.grid(row=5, column=0, padx=20, pady=10)

        #===========
        #Run
        #===========

        run_button = ctk.CTkButton(self.text_frame, text="Run Script", command=self.run_script)
        run_button.grid(row=5, column=1, padx=20, pady=10)

        #===========
        # Terminal and Control Buttons
        #===========

        # creating a label for the terminal
        self.terminal_label = ctk.CTkLabel(self.text_frame, text="Terminal", font=ctk.CTkFont(size=20, weight='bold', underline=True))
        self.terminal_label.grid(row=6, column=0, padx=20, pady=10)

        # creating a text widget for the terminal
        self.terminal = ctk.CTkTextbox(self.text_frame,  width=400, height=100, corner_radius=10, text_color='white')
        self.terminal.grid(row=7, column=0, padx=20, pady=10)



        def input_window_setting_voltage():
            input_window = ctk.CTkToplevel(self)
            input_window.transient(self)
            input_window.title("Setting Voltage")

            # Function to handle the 'ok' button click
            def handle_ok():
                voltage = voltage_entry.get()

                # Display the sentenc ein the text widget
                self.terminal.insert("end", f"\n>> pstat.set_volt({voltage})")


                command = "print('hello world')"
                output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
                output_string = output_bytes.decode('utf-8').strip()
                self.terminal.insert("end-1c", f"\n{output_string}")
                self.terminal.see("end-1c")

                input_window.destroy()

            voltage_label = ctk.CTkLabel(input_window, text="Enter Start Voltage:")
            voltage_label.grid(row=0, column=0, padx=20, pady=10)
            voltage_entry = ctk.CTkEntry(input_window)
            voltage_entry.grid(row=1, column=0, padx=20, pady=10)

            ok_button = ctk.CTkButton(input_window, text="OK", command=handle_ok)
            ok_button.grid(row=4, column=0, padx=20, pady=10)

        # creating a button to set the voltage
        self.set_voltage_button = ctk.CTkButton(self.text_frame, text="Set Voltage", command=input_window_setting_voltage)
        self.set_voltage_button.grid(row=8, column=0, padx=20, pady=10)

        # creating a button to get the voltage
        self.get_voltage_button = ctk.CTkButton(self.text_frame, text="Get Voltage", command=self.getting_volt)
        self.get_voltage_button.grid(row=9, column=0, padx=20, pady=10)

        # creating a button to get the current
        self.get_current_button = ctk.CTkButton(self.text_frame, text="Get Current", command=self.getting_curr)
        self.get_current_button.grid(row=10, column=0, padx=20, pady=10)

        # creating a button to get the voltage range
        self.get_current_button = ctk.CTkButton(self.text_frame, text="Get Voltage Range", command=self.getting_volt_range)
        self.get_current_button.grid(row=9, column=1, padx=20, pady=10)

        # creating a button to get the current range
        self.get_current_button = ctk.CTkButton(self.text_frame, text="Get Current Range", command=self.getting_curr_range)
        self.get_current_button.grid(row=10, column=1, padx=20, pady=10)

        # creating a button to get the auto connect off
        self.get_current_button = ctk.CTkButton(self.text_frame, text="Turn Auto Connect OFF", command=self.turn_auto_connect_off)
        self.get_current_button.grid(row=8, column=2, padx=20, pady=10)

        # creating a button to get the electrodes off
        self.get_current_button = ctk.CTkButton(self.text_frame, text="Turn Elec OFF", command=self.turn_electrodes_off)
        self.get_current_button.grid(row=9, column=2, padx=20, pady=10)

        # creating a button to get the electrodes on
        self.get_current_button = ctk.CTkButton(self.text_frame, text="Turn Elec ON",command=self.turn_electrodes_on)
        self.get_current_button.grid(row=10, column=2, padx=20, pady=10)



        #============================================================================================
        #============================================================================================
        #============================================================================================

        #VALVE FRAME

        self.valve_frame = ctk.CTkFrame(self, corner_radius=0)
        self.valve_frame.grid(row=0, column=3, padx=(20,20), pady=(20,0), sticky='nsew')

        self.logo_label = ctk.CTkLabel(self.valve_frame, text='Valve Control',
                                       font=ctk.CTkFont(size=20, weight='bold', underline=True))
        self.logo_label.grid(row=0, column=0, padx=20, pady=10)


        #==================
        #custom valve opening
        #==================

        def input_window_valve():
            input_window = ctk.CTkToplevel(self)
            input_window.transient(self)
            input_window.title("Valve Opening")


            # Function to handle the 'ok' button click
            def handle_ok():
                valve_number = valve_number_entry.get()
                time_duration = time_entry.get()
                command_open = f'usbrelay QMBS_{valve_number}=1'
                command_close = f'usbrelay QMBS_{valve_number}=0'


                # os.system(command_open)

                # Display the sentenc ein the text widget
                self.terminal.insert("end", f"\n>> valve {valve_number} open for {time_duration} seconds")
                self.terminal.see("end-1c")
                time.sleep(int(time_duration))


                # os.system(command_close)
                input_window.destroy()

            #create a label for the valve number
            valve_number_label = ctk.CTkLabel(input_window, text="Enter Valve Number:")
            valve_number_label.grid(row=0, column=0, padx=20, pady=10)
            valve_number_entry = ctk.CTkEntry(input_window)
            valve_number_entry.grid(row=1, column=0, padx=20, pady=10)

            time_label = ctk.CTkLabel(input_window, text="Enter Time:")
            time_label.grid(row=2, column=0, padx=20, pady=10)
            time_entry = ctk.CTkEntry(input_window)
            time_entry.grid(row=3, column=0, padx=20, pady=10)

            ok_button = ctk.CTkButton(input_window, text="OK", command=handle_ok)
            ok_button.grid(row=4, column=0, padx=20, pady=10)

        # Creating a valve status label
        custom_valve_opening_label = ctk.CTkButton(self.valve_frame, text="Custom Valve Opening", command=input_window_valve)
        custom_valve_opening_label.grid(row=2, column=0, padx=20, pady=10)



        self.logo_label = ctk.CTkLabel(self.valve_frame, text='Manual Valve Control',
                                       font=ctk.CTkFont(size=15, weight='bold', underline=True))
        self.logo_label.grid(row=4, column=0, padx=20, pady=10)

        self.valve_labels = []
        self.valve_open_buttons = []
        self.valve_close_buttons = []

        self.stopwatch_label = ctk.CTkLabel(self.valve_frame, text='00:00:00', bg_color='black', text_color='white')
        self.stopwatch_label.grid(row=14, column=0, padx=40, pady=20)
        self.start_time = 0
        self.running = False

        num_valves = 8
        for valve_num in range(1, num_valves + 1):
            valve_label = ctk.CTkLabel(self.valve_frame, text=f'Valve {valve_num} Closed', bg_color='red', text_color='black')
            valve_label.grid(row=5 + valve_num, column=0, padx=20, pady=10)
            self.valve_labels.append(valve_label)

            valve_open_button = ctk.CTkButton(self.valve_frame, text='Open',
                                              command=self.create_open_function(valve_num))
            valve_open_button.grid(row=5 + valve_num, column=1, padx=20, pady=10)
            self.valve_open_buttons.append(valve_open_button)

            valve_close_button = ctk.CTkButton(self.valve_frame, text='Close',
                                               command=self.create_close_function(valve_num))
            valve_close_button.grid(row=5 + valve_num, column=2, padx=20, pady=10)
            self.valve_close_buttons.append(valve_close_button)

        # Diamond Logo
        '''
        image = os.path.realpath('dls_logo.png')
        self.logo_image = ctk.CTkImage(Image.open(image))
        self.logo_label = ctk.CTkLabel(self.valve_frame, text="", image=self.logo_image)
        self.logo_label.grid(row=15, column=0, padx=20, pady=10)
        '''






    #===================================================================================================================
    #===================FUNCTIONS========================================================================================
    #===================================================================================================================
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def turn_on_pstat(self):
        self.status_label.configure(text='Status: ON', fg_color='green')
        # self.test.pstat.set_all_elec_connected(True)
        self.terminal.insert("end", f"\n>> pstat.set_all_elec_connected(True)")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")

    def turn_off_pstat(self):
        self.status_label.configure(text='Status: OFF', fg_color='red')
        # self.test.pstat.set_all_elec_connected(False)

        self.terminal.insert("end", f"\n>> pstat.set_all_elec_connected(False)")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")

    def set_current_range(self, value):
        # self.test.pstat.set_curr_range(value)

        self.terminal.insert("end", f"\n>> pstat.set_curr_range({value})")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")

    def set_voltage_range(self, value):
        # self.test.pstat.set_volt_range(value)

        self.terminal.insert("end", f"\n>> pstat.set_volt_range({value})")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")

    def create_open_function(self, valve_num):
        def valve_open():
            # os.system('usbrelay 6QMBS_1=1')
            if not self.running:
                self.start_time = time.time()
                self.running = True
                self.update_stopwatch()

            self.valve_labels[valve_num -1].configure(text=f'Valve {valve_num} Open', bg_color='green', text_color='black')
            print(f'Valve {valve_num} opened')
        return valve_open

    def create_close_function(self, valve_num):
        def valve_close():
            # os.system('usbrelay 6QMBS_1=0')
            if self.running:
                elapsed_time = time.time() - self.start_time
                self.running = False
                self.update_stopwatch()

            self.valve_labels[valve_num -1].configure(text=f'Valve {valve_num} Closed', bg_color='red', text_color='black')
            print(f'Valve {valve_num} closed')
        return valve_close

    def format_time(self, elapsed_time):
        hours = int(elapsed_time / 3600)
        minutes = int((elapsed_time % 3600) / 60)
        seconds = int(elapsed_time % 60)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def update_stopwatch(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            self.stopwatch_label.configure(text=self.format_time(elapsed_time))
            self.after(1000, self.update_stopwatch)

    def getting_volt(self):
        # Display the sentence in the text widget
        self.terminal.insert("end", f"\n>> pstat.get_volt()")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")
    def getting_curr(self):
        # Display the sentence in the text widget
        self.terminal.insert("end", f"\n>> pstat.get_curr()")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")
    def getting_curr_range(self):
        # Display the sentence in the text widget
        self.terminal.insert("end", f"\n>> pstat.get_curr_range()")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")
    def getting_volt_range(self):
        # Display the sentence in the text widget
        self.terminal.insert("end", f"\n>> pstat.get_volt_range()")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")

    def turn_auto_connect_off(self):
        # Display the sentence in the text widget
        self.terminal.insert("end", f"\n>> pstat.set_auto_connect(False)")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")

    def turn_electrodes_off(self):
        # Display the sentence in the text widget
        self.terminal.insert("end", f"\n>> pstat.set_all_elec_connected(False)")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")

    def turn_electrodes_on(self):
        # Display the sentence in the text widget
        self.terminal.insert("end", f"\n>> pstat.set_all_elec_connected(True)")

        command = "print('hello world')"
        output_bytes = subprocess.check_output(['python', '-c', command], shell=True)
        output_string = output_bytes.decode('utf-8').strip()
        self.terminal.insert("end-1c", f"\n{output_string}")
        self.terminal.see("end-1c")

    def run_script(self):
        script_path = '/path/of/yhe/script.py'
        subprocess.Popen(['x-terminal-emulator', '-e', 'python3', script_path])
        self.terminal.insert("end-1c", f"\n>> python3 {script_path}")
        self.terminal.see("end-1c")

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
