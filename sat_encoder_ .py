import serial
import csv
import time
from pynput import keyboard  # Replace `keyboard` with `pynput` for Linux compatibility


# Set up the Serial connection
arduino_port = '/dev/ttyUSB1'  # Update this to match the correct port for your Arduino
baud_rate = 9600              # Must match the baud rate set in the Arduino code
timeout = 2                   # Timeout for serial reading

# Output CSV file
output_file = "sat_encoder_xy.csv"

def initialize_csv(file_name):
    """Initialize the CSV file with headers."""
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x (m)", "y (m)"])  # Only x and y columns

def log_to_csv(file_name, x, y):
    """Append a line of data to the CSV file."""
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([x, y])

def parse_arduino_data(line):
    """Parse the Arduino data string into separate values."""
    try:
        # Example data format: "x: 1.23 m, y: 2.34 m, theta: 45.67"
        parts = line.decode('utf-8').strip().split(',')
        x = float(parts[0].split(':')[1].strip().replace('m', ''))
        y = float(parts[1].split(':')[1].strip().replace('m', ''))
        return x, y
    except (IndexError, ValueError) as e:
        print(f"Error parsing line: {line}. Error: {e}")
        return None, None
def wait_for_enter():
    """Wait for the user to press the 'Enter' key."""
    print("Press 'Enter' to start logging and send the signal...")

    def on_press(key):
        if key == keyboard.Key.enter:
            return False  # Stop listening when 'Enter' is pressed

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
def main():
    # Initialize the CSV file
    initialize_csv(output_file)

    try:
        with serial.Serial(arduino_port, baud_rate, timeout=timeout) as ser:
            # Wait for user to press 'Enter'
            wait_for_enter()
            ser.write(b'S')  # Send 'S' to Arduino to start
            print("Start signal sent to Arduino.")

            # Begin data logging
            print(f"Logging started. Data will be saved to '{output_file}'.")
            while True:
                line = ser.readline()
                if line:
                    x, y = parse_arduino_data(line)
                    if x is not None and y is not None:
                        log_to_csv(output_file, x, y)
                        print(f"Logged: x={x}, y={y}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nLogging stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
