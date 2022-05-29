import os 
from datetime import datetime as dt
import time
import sys
path=os.path.join(os.getcwd(),"main.exe")
while True:
    current_min=dt.now().strftime("%M")
    current_sec=dt.now().strftime("%S")
    print(dt.now().strftime("%I:%M:%S,%p"))
    time.sleep(1)
    if current_min=="00" and current_sec=="00":
        os.system(f"python {path}")
        break
sys.exit(0)
