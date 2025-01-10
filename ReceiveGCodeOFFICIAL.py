import socket
import re
import time
import sys
from pymycobot.mycobot import MyCobot
import time

###############################################################################
mc = MyCobot('/dev/ttyAMA0',1000000)
mc.power_off()
time.sleep(3)
mc.power_on()
time.sleep(3)

mc.set_color(255,0,0)
# Set interpolation mode
mc.set_fresh_mode(0)
time.sleep(0.5)
# Send the initial point angle of the robot arm
mc.send_angles([0, -40, -130, 80, 0, 50], 50)
# Wait 3 seconds for the robot arm to move to the specified angle
time.sleep(3)

mc.set_color(0,0,255)
#############################################################################
# Define host and port for the server
HOST = '10.42.0.1'  # Change to your server's IP address
PORT = 46384

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)

# Main loop
while True:
    # Accept a connection
    connection, client_address = server_socket.accept()
    

    # Initialize buffer for collecting data
    data_buffer = b''


    # Receive data from the client
    print('Entered while true')
    data = connection.recv(1024)  # Increased buffer size for potentially larger data
    if data:  
                print(f'Data Received: {data}')  # Debugging
                
                # Add received data to the buffer
                data_buffer += data
                
                # Check if buffer contains a complete set of data
                if b'Z' in data_buffer:
                    # Regular expression to find values X, Y, and Z in the string
                    pattern = rb'X(-?\d+(\.\d+)?)Y(-?\d+(\.\d+)?)Z(-?\d+(\.\d+)?)'
                    # Find matches in the input string
                    matches = re.findall(pattern, data_buffer) 
                    
                    # Iterate over the matches and display the values
                    for match in matches:
                        x = match[0] if match[0] else "Not Found"
                        y = match[1] if match[1] else "Not Found"
                        z = match[2] if match[2] else "Not Found"
                        
                        print(f'Value X: {x}\nValue Y: {y}\nValue Z: {z}\n')

                        from pymycobot.mycobot import MyCobot

                        mc = MyCobot('/dev/ttyAMA0',1000000)
                        mc.set_color(255,0,255)
                        
                        # Get the current coordinates of the robot arm
                        get_coords = mc.get_coords()
                        print("Current Coordinates:", get_coords)
                        print("get_coords[3]:", get_coords[3])
                        print("get_coords[4]:", get_coords[4])
                        print("get_coords[5]:", get_coords[5])
                                        
                        x=float(x.decode())
                        y=float(y.decode())
                        z=float(z.decode())
                        
                        print(f'Value X: {x}\nValue Y: {y}\nValue Z: {z}\n')
                        
                        coords=[x,y,z, get_coords[3], get_coords[4], get_coords[5]]

                        # Send coordinates to the robot arm one by one
                        mc.send_coords(coords, 100, 1)  # Send coordinates to the robot arm
                        time.sleep(3.5)
                        mc.set_color(255,255,0)
                                    
                    # Clear the buffer after processing
                    data_buffer = b''

print('out While')