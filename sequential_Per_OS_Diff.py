from pprint import pprint
from netmiko import ConnectHandler
from time import time
from getpass import getpass

username = input('\nUsername: ')
password = getpass()

#------------------------------------------------------------------------------
def read_devices( devices_filename ):

    devices = {}

    with open( devices_filename ) as devices_file:

        for device_line in devices_file:

            device_info = device_line.strip().split(',')

            device = {'ipaddr': device_info[0],
                      'type'  : device_info[1],
                      'name'  : device_info[2]}

            devices[device['ipaddr']] = device

    print('\nDevices : ' + '\n')
    pprint(devices)
    return devices

#------------------------------------------------------------------------------
def config_worker( device, username, password ):

    if   device['type'] == 'cisco-ios' : device_type = 'cisco_ios'
    elif device['type'] == 'cisco-nxos': device_type = 'cisco_nxos'
    else:                                device_type = 'cisco_ios'

    print('\nConnecting to device {0}'.format( device['ipaddr'] ))

    session = ConnectHandler( device_type=device_type, 
                              ip=device['ipaddr'], 
                              username=username, 
                              password=password )

    if device_type == 'cisco_ios':

        diff = []

        running_config = session.send_command('show running-config')
        running_lines = running_config.splitlines()

        for line in ios_cmds:
            if line not in running_lines:
                diff.append('+ ' + line)

        if len(diff) > 0:
            print(' -- ' + str(diff))
        else:
            print(' -- No difference ...')

    if device_type == 'cisco_nxos':

        diff = []

        running_config = session.send_command('show running-config')
        running_lines = running_config.splitlines()

        for line in nxos_cmds:
            if line not in running_lines:
                diff.append('+ ' + line)

        if len(diff) > 0:
            print(' -- ' + str(diff))
        else:
            print(' -- No difference ...')


    config_filename = 'config-' + device['ipaddr'] + '.txt'
    with open( config_filename, 'w' ) as config_out: config_out.write( running_config )
    session.disconnect()

    return

#=============================================================================
# ---- Main:
#=============================================================================

devices = read_devices( 'devices-file.txt' )

with open('nxos_commands.txt') as f:
    nxos_cmds = f.read().splitlines()

with open('ios_commands.txt') as f:
    ios_cmds = f.read().splitlines()

starting_time = time()

for ipaddr, device in devices.items():

    config_worker( device, username, password )

print('\nDone, elapsed time=', time()-starting_time)
