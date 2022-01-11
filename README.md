
# AutosshTunnel
A script to build autossh tunnel between a local machine and a server for NAT traversal.  
Run the script in local machine.

## Installation
prerequisite:  
* autossh should be installed
* local machine should be authorized by the server (e.g. by using `ssh-copy-id`)  

```bash
cd autosshTunnel
sudo chmod +x install.sh
./install.sh
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
