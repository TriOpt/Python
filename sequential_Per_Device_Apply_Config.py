from pprint import pprint
from netmiko import ConnectHandler
from time import time
from getpass import getpass

username = input('\nUsername: ')
password = getpass()


#------------------------------------------------------------------

def read_devices( devices_filename ):
    devices = {}

    with open( devices_filename ) as devices_file:

        for device_line in devices_file:

            device_info = device_line.strip().split(',')

            device = {'ipaddr': device_info[0],
                      'type'  : device_info[1],
                      'name'  : device_info[2],
                      'file'  : device_info[3]}

            devices[device['ipaddr']] = device

        print('\n----- devices --------------------------')
        pprint( devices )
        return devices

#------------------------------------------------------------------

def config_worker( device, username, password):

    if   device['type'] == 'cisco-ios' : device_type = 'cisco_ios'
    elif device['type'] == 'cisco-nxos': device_type = 'cisco_nxos'
    else:                                device_type = 'cisco_ios'
    
    device_file = device['file']

    with open( device_file ) as f:
        cmd_list = f.read().splitlines()

    print('---- Connecting to device {0}'.format( device['ipaddr'] ))

    session = ConnectHandler( device_type=device_type, ip=device['ipaddr'], username=username, password=password )

    if device_type == 'cisco_ios':
        print('---- Sending configuration ' + device['ipaddr'])
        session.send_config_set(cmd_list)
        print('---- Writing configuration ' + device['ipaddr'])
        session.save_config()

    if device_type == 'cisco_nxos':
        print('---- Sending configuration ' + device['ipaddr'])
        session.send_config_set(cmd_list)
        print('---- Writing configuration ' + device['ipaddr'])
        session.save_config()

    session.disconnect()

    return

#================================================================
# ---- Main: Sequential Configuration
#================================================================

devices = read_devices( 'devices-file.txt' )

starting_time = time()

print('\n---- Begin sequential config ----\n')
for ipaddr, device in devices.items():
    
    print('Config for: ', device)
    config_worker( device, username, password)

print('\n---- End sequential config, elapsed time=', time()-starting_time)
