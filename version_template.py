#!/usr/bin/env python

from getpass import getpass
from netmiko import ConnectHandler
from time import time
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

username = input('Username: ')
password = getpass()

starting_time = time()

#with open('4500_commands_file.txt') as f:
#    4500_commands = f.read().splitlines()

#with open('2960_commands_file.txt') as f:
#    2960_commands = f.read().splitlines()

#with open('nxos_commands_file.txt') as f:
#    nxos_command = f.read().splitlines()

with open('ios_devices_list.txt') as f:
    devices_list = f.read().splitlines()

for devices in devices_list:
    print ('\n' + 'Connecting to ' + devices )
    ip_address = devices
    ios = {
            'device_type': 'cisco_ios',
            'ip': ip_address,
            'username': username,
            'password': password,
    }
    
    try:
        net_connect = ConnectHandler(**ios)
    except (AuthenticationException):
        print('Authentication failure: ' + ip_address)
        continue
    except (NetMikoTimeoutException):
        print('Timeout to device: ' + ip_address)
        continue
    except (EOFError):
        print('End of file while attempting device ' + ip_address)
        continue
    except (SSHException):
        print('SSH Issue. Are you sure SSH is enabled? ' + ip_address)
        continue
    except Exception as unknown_error:
        print('Some other error: ' + str(unknown_error))
        continue
    
    # Types of devices
    list_version = ['cat4500e-UNIVERSALK9-M',
                    'C2960X-UNIVERSALK9-M',
                    'n3000-uk9-kickstart.6.0.2.U6.10.bin',
                    'n9000-dk9.7.0.3.I1.3.bin',
                    'nxos.7.0.3.I4.6.bin',
                    'nxos.7.0.3.I4.7.bin',
                    'nxos.7.0.3.I4.8.bin'
                    ]

    # Check software versions

    for software_ver in list_version:
        print('Checking for ' + software_ver)
        output_version = net_connect.send_command('show version')
        int_version = 0 # Reset integer value
        int_version = output_version.find(software_ver) #Check software version
        if int_version > 0:
            print('Software version found: ' + software_ver)
            break
        else:
            print('Did not find ' + software_ver)

#    if software_ver == 'cat4500e-UNIVERSALK9-M':
#        print('Running ' + software_ver + ' commands')
#        output = net_connect.send_config_set(4500_commands)
#    elif software_ver == 'C2960X-UNIVERSALK9-M':
#        print('Running ' + software_ver + ' commands')
#        output = net_connect.send_config_set(2960_commands)
#    elif software_ver == 'n3000-uk9-kickstart.6.0.2.U6.10.bin':
#        print('Running ' + software_ver + ' commands')
#        output = net_connect.send_config_set(n3k_commands)
#    elif software_ver == 'n9000-dk9.7.0.3.I1.3.bin':
#        print('Running ' + software_ver + ' commands')
#        output = net_connect.send_config_set(n9k_commands)
#    elif software_ver == 'nxos.7.0.3.I4.6.bin':
#        print('Running ' + software_ver + ' commands')
#        output = net_connect.send_config_set(n3k_commands)
#    elif software_ver == 'nxos.7.0.3.I4.7.bin':
#        print('Running ' + software_ver + ' commands')
#        output = net_connect.send_config_set(n3k_commands)
#    elif software_ver == 'nxos.7.0.3.I4.8.bin':
#        print('Running ' + software_ver + ' commands')
#        output = net_connect.send_config_set(n3k_commands)
#    print(output)

print('\n' + '----- End, elapsed time', time() - starting_time)
