import subprocess

proc = subprocess.Popen("grep -rn Base /",stdout=subprocess.PIPE, shell=True)
while True:
    line = proc.stdout.readline()
    if not line:
        break
    #the real code does filtering here
    print(line.rstrip())