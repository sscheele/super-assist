import subprocess
import sys
with open('test.log', 'w') as f:
    process = subprocess.Popen(["../GAssist/env/bin/google-assistant-demo"], stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        f.write(line)