import subprocess
import time
proc = subprocess.Popen(["ssh", "-tt", "pi@127.0.0.1"],
                        stdout=subprocess.PIPE, stdin=subprocess.PIPE)
time.sleep(10)
proc.stdin.write(b"/home/pi/Desktop/GAssist/env/bin/google-assistant-demo\n")
proc.stdin.flush()
while True:
    next_line = proc.stdout.readline()
    if next_line != '':
        # the real code does filtering here
        print(next_line.decode("utf-8"), end='')
    else:
        time.sleep(.01)
