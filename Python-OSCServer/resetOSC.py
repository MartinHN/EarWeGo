import subprocess,os
result = subprocess.check_output("ps -A | grep 'Python'", shell=True)
# print result;
lines = result.split('\n');
for l in lines:
	if l.split(' ')[12][:10] =='/usr/local':
		os.system("kill "+l.split(' ')[1])