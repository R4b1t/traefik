#!/usr/bin/env python3

import os
import subprocess

# Read user input
username = input("Enter username: ")
server_ip = input("Enter server IP address: ")
use_password = input("Are you using a password instead of SSH keys? [y/n]: ")
domain_name = input("Enter the domain name: ")
cloudflare_email = input("Enter the Cloudflare email for traefik: ")
cloudflare_api_key = input("Enter the Cloudflare API key for traefik: ")
traefik_user_hash = input("Enter traefik dashboard user hash: ")

# Replace values in vars.yml file
with open('group_vars/all/vars.yml', 'r') as f:
    content = f.read()
content = content.replace('<username>', username)
content = content.replace('<server_ip>', server_ip)
content = content.replace('<domain_name>', domain_name)
content = content.replace('<cloudflare_email>', cloudflare_email)
content = content.replace('<cloudflare_api_key>', cloudflare_api_key)
content = content.replace('<traefik_basic_auth_hash>', traefik_user_hash)
with open('group_vars/all/vars.yml', 'w') as f:
    f.write(content)

# Replace values in inventory file
with open('inventory', 'r') as f:
    content = f.read()
content = content.replace('<server_ip>', server_ip)
content = content.replace('<username>', username)
if use_password == 'y':
    ssh_password = input("Enter SSH password: ")
    content = content.replace(
        'ansible_ssh_private_key_file = <path/to/private/key>', '')
    content += f'ansible_ssh_pass = {ssh_password}\n'
else:
    private_key_path = input("Enter path to private key: ")
    content = content.replace('<path/to/private/key>', private_key_path)
with open('inventory', 'w') as f:
    f.write(content)

# Run the playbook
subprocess.run(['ansible-playbook', 'main.yml'])
