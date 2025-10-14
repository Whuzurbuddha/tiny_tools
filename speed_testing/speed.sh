#!/bin/bash
today=$(date '+%d:%m:%Y')
time=$(date '+%H:%M')
speed=""
while [[ -z "$speed" ]]; do
    speed=$(speedtest --no-upload | grep Download | awk '{print $2}')
    if [[ -z "$speed" ]]; then
        sleep 10
    fi
done
mysql -u $user -p $password speedtesting <<EOF
INSERT INTO testings (test_date, test_time, speed)
VALUES ('$today', '$time', '$speed');
EOF
