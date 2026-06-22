import psutil
import time

while True:
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    print(f'CPU = {cpu}% , Mem = {memory}%')
    time.sleep(5)

    if cpu > 80:
        print("Alert CPU High")
    if memory>90:
        print("Alert Memory High")