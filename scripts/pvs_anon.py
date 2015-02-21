#!/usr/bin/env python
import sys
import re

pvs_anon = open(sys.argv[1] + '.ANON.html', 'w')
with open(sys.argv[1]) as pvs_original:
    pvs_anon.write(re.sub(r'\.\d{1,3}\.\d{1,3} \(', '.XXX.XXX (', 
                          pvs_original.read()))
pvs_anon.close()