import serial
import csv
import time
import keyboard  # Install this library with `pip install keyboard`

# Set up the Serial connection
arduino_port = '/dev/ttyUSB1'  # Update this to match the correct port for your Arduino
baud_rate = 9600              # Must match the baud rate set in the Arduino code
timeout = 2                   # Timeout for serial reading

# Output CSV file
output_file = "arduino_positions_xy.csv"

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

def main():
    # Initialize the CSV file
    initialize_csv(output_file)
    print(f"Waiting to send start signal. Press 'Enter' to start logging and send the signal...")

    try:
        with serial.Serial(arduino_port, baud_rate, timeout=timeout) as ser:
            # Wait for key press to send start signal
            while True:
                if keyboard.is_pressed('enter'):
                    ser.write(b's')  # Send 's' to Arduino
                    print("Start signal sent to Arduino.")
                    break

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
