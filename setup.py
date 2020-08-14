import os
import sys

r = sys.argv[1]

if(r == 'install'):
  cmd1 = 'curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
  cmd2 = 'python get-pip.py'
  os.system(cmd1)
  os.system(cmd2)
else:
  print("Please write install on the command line")
  exit()

