"""A module for interacting with the Seeed Studio Relay board for the Raspberry Pi."""
# =========================================================
# Seeed Studio Raspberry Pi Relay Board Library
#
# by John M. Wargo (www.johnwargo.com)
#
# Modified from the sample code on the Seeed Studio Wiki
# http://wiki.seeed.cc/Raspberry_Pi_Relay_Board_v1.0/
# =========================================================

from __future__ import print_function

import smbus

# The number of relay ports on the relay board.
# This value should never change!
NUM_RELAY_PORTS = 4

# Change the following value if your Relay board uses a different I2C address. 
DEVICE_ADDRESS = 0x20  # 7 bit address (will be left shifted to add the read write bit)

# Don't change the values, there's no need for that.
DEVICE_REG_MODE1 = 0x06
DEVICE_REG_DATA = 0xff

bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


def relay_on(relay_num):
    """Turn the specified relay (by relay #) on.

    Call this function to turn a single relay on.
    
    Args:
        relay_num (int): The relay number that you want turned on.        
    """
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    if isinstance(relay_num, int):
        # do we have a valid relay number?
        if 0 < relay_num <= NUM_RELAY_PORTS:
            print('Turning relay', relay_num, 'ON')
            DEVICE_REG_DATA &= ~(0x1 << (relay_num - 1))
            bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
        else:
            print('Invalid relay #:', relay_num)
    else:
        print('Relay number must be an Integer value')


def relay_off(relay_num):
    """Turn the specified relay (by relay #) off.

    Call this function to turn a single relay off.
    
    Args:
        relay_num (int): The relay number that you want turned off.
    """
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    if isinstance(relay_num, int):
        # do we have a valid relay number?
        if 0 < relay_num <= NUM_RELAY_PORTS:
            print('Turning relay', relay_num, 'OFF')
            DEVICE_REG_DATA |= (0x1 << (relay_num - 1))
            bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)
        else:
            print('Invalid relay #:', relay_num)
    else:
        print('Relay number must be an Integer value')


def relay_all_on():
    """Turn all of the relays on.

    Call this function to turn all of the relays on.        
    """
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    print('Turning all relays ON')
    DEVICE_REG_DATA &= ~(0xf << 0)
    bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)


def relay_all_off():
    """Turn all of the relays on.

    Call this function to turn all of the relays on.        
    """
    global DEVICE_ADDRESS
    global DEVICE_REG_DATA
    global DEVICE_REG_MODE1

    print('Turning all relays OFF')
    DEVICE_REG_DATA |= (0xf << 0)
    bus.write_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1, DEVICE_REG_DATA)


def relay_toggle_port(relay_num):
    """Toggle the specified relay (on to off, or off to on).

    Call this function to toggle the status of a specific relay.
    
    Args:
        relay_num (int): The relay number to toggle.
    """
    print('Toggling relay:', relay_num)
    if relay_get_port_status(relay_num):
        # it's on, so turn it off
        relay_off(relay_num)
    else:
        # it's off, so turn it on
        relay_on(relay_num)


def relay_get_port_status(relay_num):
    """Returns the status of the specified relay (True for on, False for off)
  
    Call this function to retrieve the status of a specific relay.
      
    Args:
        relay_num (int): The relay number to query.
    """
    # determines whether the specified port is ON/OFF
    global DEVICE_REG_DATA
    print('Checking status of relay', relay_num)
    res = relay_get_port_data(relay_num)
    if res > 0:
        mask = 1 << (relay_num - 1)
        # return the specified bit status
        # return (DEVICE_REG_DATA & mask) != 0
        return (DEVICE_REG_DATA & mask) == 0
    else:
        # otherwise (invalid port), always return False
        print("Specified relay port is invalid")
        return False


def relay_get_port_data(relay_num):
    """Internal function, used to retrieve binary data from the relay board.
        
    Args:
        relay_num (int): The relay port to query.
    """
    # gets the current byte value stored in the relay board
    global DEVICE_REG_DATA
    print('Reading relay status value for relay', relay_num)
    # do we have a valid port?
    if 0 < relay_num <= NUM_RELAY_PORTS:
        # read the memory location
        DEVICE_REG_DATA = bus.read_byte_data(DEVICE_ADDRESS, DEVICE_REG_MODE1)
        # return the specified bit status
        return DEVICE_REG_DATA
    else:
        # otherwise (invalid port), always return 0
        print("Specified relay port is invalid")
        return 0
