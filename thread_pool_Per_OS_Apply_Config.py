from pprint import pprint
from netmiko import ConnectHandler
import json
from time import time
from getpass import getpass

from multiprocessing.dummy import Pool as ThreadPool

#device_creds = dict()

username = input('\nUsername: ')
password = getpass()

#device_creds[username] = password

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
def config_worker( device ):

    #---- Connect to device ----
    if   device['type'] == 'cisco-ios' : device_type = 'cisco_ios'
    elif device['type'] == 'cisco-nxos': device_type = 'cisco_nxos'
    else:                                device_type = 'cisco_ios'    # attempt Cisco IOS as default

    print('---- Connecting to device {0}'.format( device['ipaddr'] ))
    
    #---- Connect to device ----
    session = ConnectHandler( device_type=device_type, ip=device['ipaddr'], username=username, password=password )

    if device_type == 'cisco_ios':
        print('---- Sending configuration ' + device['ipaddr'])
        session.send_config_set('ios_cmds')
        print('---- Writing configuration ' + device['ipaddr'])
        session.save_config()

    if device_type == 'cisco_nxos':
        print('---- Sending configuration ' + device['ipaddr'])
        session.send_config_set('nxos_cmds')
        print('---- Writing configuration ' + device['ipaddr'])
        session.save_config()

    session.disconnect()

    return

#=============================================================================
# ---- Main: Get Configuration
#=============================================================================

devices = read_devices( 'devices-file.txt' )

with open('nxos_commands.txt') as f:
    nxos_cmds = f.read().splitlines()

with open('ios_commands.txt') as f:
    ios_cmds = f.read().splitlines()

num_threads_str = input('\nNumber of threads (5): ') or '5'
num_threads     = int( num_threads_str )

#---- Create list for passing to worker
config_params_list = []
for ipaddr,device in devices.items():
    config_params_list.append( ( device ) )

starting_time = time()

print('\n---- Creating threadpool, launching threads\n')
threads = ThreadPool( num_threads )
results = threads.map( config_worker, config_params_list )

threads.close()
threads.join()

print('\n---- End, elapsed time=', time() - starting_time)
