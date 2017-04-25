#!/bin/sh
/usr/bin/dumpcap -i eth1 -P -w - | /usr/bin/tshark -T psml -PS -l -r -