#!/bin/bash

LOGFILE="/Users/user/loadlogger/loadlog-"`date "+%b%g"`

echo -n `date "+%m/%d/%y"` " ">>$LOGFILE 2>&1
echo -n `uptime` >>$LOGFILE 2>&1
echo -n -e "\t" >>$LOGFILE 2>&1

#Number of users with GUI sessions
echo -n `w | grep console |wc -l` >>$LOGFILE 2>&1
echo -n -e "\t" >>$LOGFILE 2>&1

#Is screenlock running?
echo -n `ps -ax | grep ScreenSaver | grep -v grep | wc -l` >>$LOGFILE 2>&1
echo  >>$LOGFILE 2>&1
