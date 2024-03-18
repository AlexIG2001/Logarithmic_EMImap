from tkinter import *
import customtkinter
import tkinter
from tkinter import filedialog
import os
import serial.tools.list_ports
from customtkinter import CTkLabel, CTk, CTkTextbox, CTkFrame,CTkScrollbar

# Define the target folder path (replace with your desired path)
target_folder_path = "D:/Diploma Project/EMI_mapper-master/output"


#set theme
customtkinter.set_appearance_mode("dark")

#create CTk window
root=customtkinter.CTk()
root.title("Emi Mapper")

#Setting window width and Height
root.geometry("800x650")

#Use CTk button instead of Tkinter button

def button_event_start():
    print("Here will be the start button")

#butonul de start
button = customtkinter.CTkButton(master=root, text="Start", command=button_event_start,hover_color="#2ECC71")
button.pack(padx=100, pady=50,anchor=CENTER)
#button.place(relx=0.5,rely=0.5,anchor=CENTER)


def button_event_output():
    # Check if the folder exists
    if os.path.exists(target_folder_path):
        # Open the folder using the system's default application
        os.startfile(target_folder_path)
    else:
        # Display an error message if the folder doesn't exist
        message = CTkLabel(master=root, text="Folder not found!", text_color="red")
        message.pack(pady=10)

#buttonul de galerie rezultate
button = customtkinter.CTkButton(master=root, text="Gallery", command=button_event_output,hover_color="#2ECC71")
button.pack(padx=100, pady=50)
#button.place(relx=0.5,rely=0.5,anchor=CENTER)



#butonul de help
def button_event_help():

        # Create a new window for the help content
        help_window = CTk()
        help_window.title("Instructions")
        help_window.geometry("800x800")

        # Create a label to display the instructions
        help_window_label = CTkLabel(
            master=help_window,
            text="""
            **KEYBINDINGS:**
                * Press "s" to select the probe.
                * Press "r" to reset.
                * Press "q" to display the EMI map and exit.

            **How to use the script:**
                1. Select the COM port your DAQ is connected to.
                2. Launch the script by pressing the start button.
                3. Before selecting the script, position the camera in a stable way and the DUT and the probe and press the RESET (r) button.
                4. Now press the SELECT (s) button and with your LEFT-CLICk button on the mouse select the probe head.
                5. Press "Space" or "Enter" after you selected the probe head.
                6. Move the probe above the DUT.
                7. Press Q to see the result.
            """,
            text_color="white",
            font=("Calibri", 24,"bold"),  # Different font
            width=200,
            height=50


        )
        help_window_label.pack(padx=20, pady=20,anchor='center')

        help_window.mainloop()


button = customtkinter.CTkButton(master=root, text="Help", command=button_event_help,hover_color="#2ECC71")
button.pack(padx=100, pady=50)
#button.place(relx=0.5,rely=0.5,anchor=CENTER)


def button_event_com():
    comports_list = serial.tools.list_ports.comports()
    # Create a new window for displaying COM ports
    com_window = CTk()
    com_window.title("COM Ports")
    com_window.geometry("400x300")
    # Create a label to display the list of ports
    com_list_label = CTkLabel(master=com_window, text="")
    com_list_label.pack(padx=20, pady=20)
    # Generate formatted text with port information
    ports_info = ", ".join(f"{port.device} ({port.description})" for port in comports_list)
    com_list_label.configure(text=f"Available COM ports: {ports_info}",text_color='white')
    com_window.mainloop()
#butonul de display com port

button = customtkinter.CTkButton(master=root, text="COM ports", command=button_event_com,hover_color="#2ECC71")
button.pack(padx=100, pady=50,anchor=CENTER)
#button.place(relx=0.5,rely=0.5,anchor=CENTER)


#running the GUI


root.mainloop()


