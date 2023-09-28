#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/root/tasmota2venus-mqtt
python tasmota2venus-mqtt.py
cd /



@reboot sh /home/root/tasmota2venus-mqtt/tasmota2venus-mqtt_launcher.sh >/home/root/tasmota2venus-mqtt/logs/cronlog 2>&1

