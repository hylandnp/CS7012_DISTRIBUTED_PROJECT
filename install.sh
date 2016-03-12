#!/bin/bash   

sudo apt-get install python-pip
sudo apt-get install python-virtualenv
sudo apt-get install python-dev
virtualenv env
source env/bin/activate
sudo apt-get install snmpd
sudo pip install pysnmp
pip install -r requirements.txt