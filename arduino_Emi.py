import os
import time
import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np
import serial
import sys
from scipy.ndimage.filters import gaussian_filter
from tkinter import *
import customtkinter
import serial.tools.list_ports
from customtkinter import CTkLabel, CTk, CTkTextbox, CTkFrame,CTkScrollbar
from scipy.ndimage import gaussian_filter





# Define the target folder path (replace with your desired path)
target_folder_path = "D:/Diploma Project/EMI_mapper-master/output"

#set theme
customtkinter.set_appearance_mode("dark")

#create CTk window
root=customtkinter.CTk()
root.title("Emi Mapper")

#Setting window width and Height
root.geometry("800x650")



def button_event_start():
    #if __name__ == "__main__":
        main()
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
                1.Select the COM port your DAQ is connected to.
                2. 
                3.Properly position the device under test (DUT) in the camera image,
                4.Press "R" to set the position (the camera and DUT must not move after pressing "R"),
                5.Put the probe in the frame, press "S", select the probe with the mouse and press "ENTER" to start the scanning,
                6.Scan the DUT by moving the probe,
                7.Press "Q" to exit. If a scan was made, the result is displayed.
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



def gaussian_with_nan(U, sigma=7):
    """Computes the gaussian blur of a numpy array with NaNs.
    """
    np.seterr(divide='ignore', invalid='ignore')
    V = U.copy()
    V[np.isnan(U)] = 0
    VV = gaussian_filter(V, sigma=sigma)

    W = 0 * U.copy() + 1
    W[np.isnan(U)] = 0
    WW = gaussian_filter(W, sigma=sigma)

    return VV / WW




"""""""""""
def get_port_name():
    
    port=os.getenv("COM_PORT")
    if port is None:
        port=input("Enter COM port name (e.g. COMx) where x is the number of the port: ")
        os.environ["COM_PORT"]=port
    return port
"""""""""""

def get_user_input():
  """
  This function creates a dialog window and retrieves user input.
  """
  dialog = customtkinter.CTkInputDialog(
      text="COMx:",
      title="Select COM PORT",
      fg_color="black"  # Text color
  )
  user_input = dialog.get_input()  # Get the input

  # Process the user input here (optional)

  # Close the main window after getting input (optional)
  # root.destroy()  # Uncomment this line if you want to close the script after input

  return user_input











def get_RMS_power(port=get_user_input(), baudrate=230400):
    ser = serial.Serial(port, baudrate)

    try:
        ser.flushInput()
        ser.reset_input_buffer()

        while True:
            ser.reset_input_buffer()
            data_str = ser.readline().decode('utf-8').strip()

            try:
                data_float = float(data_str)
                yield data_float
            except ValueError as e:
                print(f"Error converting data to float: {e}")
                sys.exit(0)
    finally:
        ser.close()


def main():
    print("Usage:")
    print("    * Press s to select the probe.")
    print("    * Press r to reset.")
    print("    * Press q to display the EMI map and exit.")




    # read from specified webcam  s
    cap = cv2.VideoCapture(0)

    if cap is None or not cap.isOpened():
        print('Error: unable to open video source: ')
    else:
        time.sleep(2.0)

    powermap = None
    firstFrame = None
    firstFrameMask = None

    # Init OpenCV object tracker objects
    #tracker = cv2.TrackerCSRT_create()
    tracker=cv2.legacy.TrackerCSRT_create()
    #tracker = cv2.TrackerCSRT_create()
    init_tracking_BB = None

    power_generator = get_RMS_power()

    while True:
        ret, frame = cap.read()

        if ret == False or frame is None:
            break

        frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)

        if firstFrame is None:
            firstFrame = frame
            firstFrameMask = gray
            powermap = np.empty((len(frame), len(frame[0])))
            powermap.fill(np.nan)
            continue

        frameDelta = cv2.absdiff(firstFrameMask, gray)
        thresh = cv2.threshold(frameDelta, 15, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)

        if init_tracking_BB is not None:
            (success, box) = tracker.update(thresh)

            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                data_value = next(power_generator)
                print("RMS power", data_value, "dBm at", x + w / 2, ";", y + h / 2)
                powermap[int(y + h / 4):int(y + h / 4 * 3), int(x + w / 4):int(x + w / 4 * 3)] = data_value

        frame[:, :, 2] = np.where(np.isnan(powermap), frame[:, :, 2], 255 / 2)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s") and init_tracking_BB is None:
            init_tracking_BB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
            tracker.init(thresh, init_tracking_BB)
        elif key == ord("q"):
            break
        elif key == ord("r"):
            firstFrame = None

    cap.release()
    cv2.destroyAllWindows()


    if init_tracking_BB is not None and powermap is not None and firstFrame is not None:
        blurred = gaussian_with_nan(powermap, sigma=7)
        plt.imshow(cv2.cvtColor(firstFrame, cv2.COLOR_BGR2RGB))
        im=plt.imshow(blurred, cmap='hot', interpolation='nearest', alpha=0.55)

        cbar = plt.colorbar(im, fraction=0.046, pad=0.1, orientation='vertical')
        cbar.set_label('Intensity', fontsize=12, labelpad=10)  # Adjust label properties

        #plt.axis('off')
        plt.title(
            "EMI map (min. " + "%.2f" % np.nanmin(powermap) + " dBm, max. " + "%.2f" % np.nanmax(powermap) + " dBm)")
        plt.show()
    else:
        print("Warning: nothing captured, nothing to do")

root.mainloop()



