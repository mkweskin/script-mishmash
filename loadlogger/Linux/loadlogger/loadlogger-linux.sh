#!/bin/bash

LOGFILE="/home/user/loadlogger/loadlog-"`date "+%b%g"`

echo -n `date "+%m/%d/%y"` >> $LOGFILE 2>&1
echo -n -e "\t" >> $LOGFILE 2>&1
uptime >> $LOGFILE 2>&1
