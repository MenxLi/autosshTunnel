#!/usr/bin/bash

THIS_DIR=$(dirname $BASH_SOURCE)
ROOT_CONF=/etc/.connectPorts_conf.json

sudo cp $THIS_DIR/connectPorts.py /usr/bin/connectPorts
sudo chmod a+x /usr/bin/connectPorts

if [ ! -f $ROOT_CONF ]
then
    sudo cp $THIS_DIR/.connectPorts_conf.json $ROOT_CONF
else
    # to prevent overwrite ROOT_CONF
    echo "$ROOT_CONF exists & will not be updated, uninstall before running this script."
fi

# sudo cp $THIS_DIR/connectBasePort.service /etc/systemd/system/
# sudo chmod u+x /etc/systemd/system/connectBasePort.service

echo "Finished."
