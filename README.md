
# AutosshTunnel
A script to build autossh tunnel between a local machine and a server for NAT traversal.  
Run the script in local machine.

## Installation
```bash
# ssh-keygen
ssh-copy-id <user_name>@<server_ip>
sudo apt install autossh
cd autosshtunnel
sudo chmod +x install.sh uninstall.sh
sudo ./install.sh
```

## Configure
Configure server IP, user name and port connection
```bash
sudo vim /etc/.connectPorts_conf.json
```
Or, make a user-level configuration file:
```bash
sudo cp /etc/.connectPorts_conf.json ~
vim ~/.connectPorts_conf.json
```

## Usage
```bash
connectPorts start
connectPorts stop
connectPorts restart
```