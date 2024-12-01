from dynamixel_sdk import *  # Uses Dynamixel SDK library
import keyboard


### Dynamixel SDK setup ### 
# Default setting
PORT = 'COM4'                       # Windows port name
# PORT = '/dev/ttyUSB0'             # Port name (/dev/ttyUSB0 for Linux)
DXL_ID = 3                          # Dynamixel ID
BAUDRATE = 1000000                  # Dynamixel default baudrate
PROTOCOL_VERSION = 2.0              # Dynamixel X series use protocol 2.0
TORQUE_ENABLE = 1                   # Value for enabling the torque
TORQUE_DISABLE = 0                  # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE = 0      # Min position (0 degrees)
DXL_MAXIMUM_POSITION_VALUE = 4095   # Max position (360 degrees)
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold
GOAL_VELOCITY = 10                  # Goal velocity

# Control table addresses for Dynamixel X series
ADDR_TORQUE_ENABLE = 64
ADDR_GOAL_POSITION = 116
ADDR_PRESENT_POSITION = 132
ADDR_GOAL_VELOCITY = 104
ADDR_PROFILE_VELOCITY = 112
ADDR_PROFILE_ACCELERATION = 108 

# Data Byte Length
LEN_GOAL_POSITION = 4
LEN_PRESENT_POSITION = 4

def angle_to_position(angle):
    return int((angle + 180) * (4095 / 360))    


def setup_dynamixel():
    # Initialize PortHandler instance
    portHandler = PortHandler(PORT)

    # Initialize PacketHandler instance
    packetHandler = PacketHandler(PROTOCOL_VERSION)

    # Open port
    if not portHandler.openPort():
        print(f"Failed to open the port: {PORT}")
        quit()

    # Set port baudrate
    if not portHandler.setBaudRate(BAUDRATE):
        print(f"Failed to change the baudrate: {BAUDRATE}")
        quit()

    # Enable Dynamixel torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed to enable torque: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Torque enable error: {packetHandler.getRxPacketError(dxl_error)}")

    # Set goal velocity
    set_velocity(portHandler, packetHandler, GOAL_VELOCITY)
    return portHandler, packetHandler

def set_velocity(portHandler, packetHandler, velocity):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_VELOCITY, velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed to set goal velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Goal velocity setting error: {packetHandler.getRxPacketError(dxl_error)}")

def main():
    portHandler, packetHandler = setup_dynamixel() # Setup Dynamixel
    try:
        while True:
            if keyboard.is_pressed('d'):
                position = angle_to_position(30)
                packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, position)
            elif keyboard.is_pressed('a'):
                position = angle_to_position(-30)
                packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, position)
            elif keyboard.is_pressed('s'):
                position = angle_to_position(0)
                packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, position)
            else:
                continue

    except KeyboardInterrupt:
        # Disable Dynamixel torque before exiting
        packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
        print("Torque disabled")

    finally:
        # Close port
        portHandler.closePort()

if __name__ == "__main__":
    main()


