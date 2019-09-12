#! /usr/bin/env python

"""
create network configurations combining CSV data with Jinja templates

"""

import csv
from jinja2 import Template

source_file = input('\nSource CSV file: ')
interface_template_file = 'template3.j2'

# String that will hold final full configuration of all interfaces
interface_configs = ''

# Open Jinja template file (as text) then create Jinja Template object
with open(interface_template_file) as f:
    interface_template = Template(f.read(), keep_trailing_newline=True)

# Open up CSV file containing data
with open(source_file) as f:
    # Use DictReader to access data from CSV
    reader = csv.DictReader(f)
    # For each row in CSV, generate interface configuration using Jinja template
    for row in reader:
        interface_config = interface_template.render(
                Interface = row['Interface'],
                New_Name = row['New-Name'],
                Model = row['Model'],
                ID = row['ID']
        )
        
        # Append interface configuration to full configuration
        interface_configs += interface_config

# Save final configuration to file
with open(source_file + '-interface-conf.txt', 'w') as f:
    f.write(interface_configs)


