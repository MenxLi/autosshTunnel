#!/usr/bin/bash

THIS_DIR=$(dirname $BASH_SOURCE)
sudo cp $THIS_DIR/connectPorts.py /usr/bin/connectPorts
sudo chmod 777 /usr/bin/connectPorts
sudo cp $THIS_DIR/.connectPorts_conf.json /etc/.connectPorts_conf.json
echo "Finished."