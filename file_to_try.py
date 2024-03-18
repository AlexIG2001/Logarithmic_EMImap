import serial
import time

def get_RMS_power(port='COM8', baudrate=115200, interval_seconds=1):
    # Create a serial object
    ser = serial.Serial(port, baudrate)

    # flush any junk left in the serial buffer
    ser.flushInput()
    ser.reset_input_buffer()  # for pyserial 3.0+

    run = True

    while run:
        start_time = time.time()  # Record the start time
        ser.reset_input_buffer()
        data_str = ser.readline().decode('utf-8').strip()  # Strip any leading/trailing whitespaces

        try:
            data_float = float(data_str)
            print("Received data:", data_float)
        except ValueError as e:
            print(f"Error converting data to float: {e}")

        elapsed_time = time.time() - start_time  # Calculate elapsed time
        print(f"Time elapsed: {elapsed_time:.4f} seconds")

        time.sleep(interval_seconds)  # Introduce a delay

if __name__ == "__main__":
    get_RMS_power()
