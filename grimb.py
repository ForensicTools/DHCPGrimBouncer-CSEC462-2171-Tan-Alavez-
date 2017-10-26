########################################################################
###
### file: grimb.py
###
### Implementation script for Grim Bouncer 
###
### 
###
### authors: Benny Tan bt4168, Jhony Alavez jia2707
###
########################################################################

import sys
import os
import re

readfile = open("test.webtest", 'r')

for line in readfile:
    lst = line.split("<Request", "</Request>")
##    if(re.findall(r'Upgrade-Insecure-Requests', line)):
##        print(lst)
    print(lst)

readfile.close()
