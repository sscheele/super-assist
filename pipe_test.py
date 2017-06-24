import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
ssh.connect('127.0.0.1', username='pi', 
    password='')
stdin, stdout, stderr = ssh.exec_command("/home/pi/Desktop/GAssist/env/bin/google-assistant-demo")
for line in stdout:
    print(line)