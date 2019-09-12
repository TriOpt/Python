from pprint import pprint
from netmiko import ConnectHandler
import json
from time import time
from getpass import getpass

username = input('\nUsername: ')
password = getpass()

#------------------------------------------------------------------------------
def read_devices( devices_filename ):

    devices = {} # create our dictionary for storing devices and their info

    with open( devices_filename ) as devices_file:

        for device_line in devices_file:

            device_info = device_line.strip().split(',') # extract device info from line

            device = {'ipaddr': device_info[0],
                      'type'  : device_info[1],
                      'name'  : device_info[2]} # create dictionary of device objects

            devices[device['ipaddr']] = device # store device in devices dictionary
                                               # note the key for devices dictionary entries is ipaddr

        print('\n----- devices --------------------------')
        pprint( devices )
        return devices

#------------------------------------------------------------------------------
def config_worker( device, username, password ):

    #---- Connect to device ----
    if   device['type'] == 'cisco-ios' : device_type = 'cisco_ios'
    elif device['type'] == 'cisco-nxos': device_type = 'cisco_nxos'
    else:                                device_type = 'cisco_ios'    # attempt Cisco IOS as default

    print('---- Connecting to device {0}'.format( device['ipaddr'] ))
    
    #---- Connect to device ----
    session = ConnectHandler( device_type=device_type, ip=device['ipaddr'], username=username, password=password )

    if device_type == 'cisco_ios':
        print('---- Sending conf ' + device['ipaddr'])
        session.send_config_set('ios_cmds')
        print('---- Writing conf ' + device['ipaddr'])
        session.save_config()
    
    if device_type == 'cisco_nxos':
        print('---- Sending conf ' + device['ipaddr'])
        session.send_config_set('nxos_cmds')
        print('---- Writing conf ' + device['ipaddr'])
        session.save_config()

    session.disconnect()

    return

#=============================================================================
# ---- Main: Apply Configuration
#=============================================================================

devices = read_devices( 'devices-file.txt' )

with open('nxos_commands.txt') as f:
    nxos_cmds = f.read().splitlines()

with open('ios_commands.txt') as f:
    ios_cmds = f.read().splitlines()

starting_time = time()

print('\n---- Begin sequential configuration ----')
for ipaddr,device in devices.items():

    print('\nInitializing ', device)
    config_worker( device, username, password )

print('\n---- End, elapsed time=', time()-starting_time)
