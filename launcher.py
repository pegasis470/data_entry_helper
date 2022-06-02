import subprocess as sp
import os
import sys
import datetime
path=os.path.join(os.getcwd(),"main.exe")
print("please wait we are configuring temp and system files main.exe will be launched soon ")
print("please close this window after main is launched")
while True:
    now=datetime.datetime.now().strftime("%S")
    if now == "23":
        os.system(path)
        break
sys.exit()
sys.exit(0)
