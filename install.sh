#!/usr/bin/bash

THIS_DIR=$(cd $(dirname $BASH_SOURCE) && pwd)
ROOT_CONF=/etc/.connectPorts_conf.json

# sudo cp $THIS_DIR/connectPorts.py /usr/bin/connectPorts

# run with current python interpreter
sudo touch /usr/bin/connectPorts
sudo echo "python3 $THIS_DIR/connectPorts.py \$1 \$2 \$3 \$4 \$5 \$6 \$7 \$8 \$9" > /usr/bin/connectPorts
sudo chmod a+x /usr/bin/connectPorts
echo "Installed connectPorts to /usr/bin/connectPorts"

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
