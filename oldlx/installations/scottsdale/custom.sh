#!/bin/bash

CRONSTRING=$(crontab -l)
LIGHTS=$"lights_on"

if [[ "$CRONSTRING" != *"$LIGHTS"* ]];  then
        (crontab -l 2>/dev/null; echo "0 18 * * * /home/entwined/Entwined/ddptest/lights_on.sh") | crontab -
        (crontab -l 2>/dev/null; echo "0 22 * * * cd /home/entwined/Entwined/ddptest/; ./lights_out.sh") | crontab -
        echo "Creating cron jobs to turn lights on and off"
fi




sudo ln -sf /usr/share/zoneinfo/US/Arizona /etc/localtime
echo "Changing TZ to Arizona local time"

echo "Adding statuscake"
if [[ "$CRONSTRING" != *"statuscake"* ]];  then
        (crontab -l 2>/dev/null; echo "*/5 * * * * /home/entwined/Entwined/oldlx/pi_setup/tunnel/statuscake.sh") | c$fi