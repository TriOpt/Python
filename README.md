# Python
Basic Netmiko scripts to apply and backup configuration to IOS and NX-OS. The backup scripts are from David Bombals' Python for Network Engineers course which I immediately began modifying for my use by adding:

- the ability to send configuration in addition to backing up the running config
- 'Per Device' functionality allowing the user to send unique configuration commands to multiple devices 

The scripts are grouped by how the netmiko function processes the list of devices

- Sequential: Iterate through list of devices one at a time
- Threaded: Generate a process for each device in the list simultaneously
- Thread Pool: Allow the user to define the amount of threads to use at execution

Each category of script contains some variety in function

- Per OS: Commands (or files containing) are selected conditionally by device OS 
- Per Device: Allows the user to supply a unique file of commands for each device
