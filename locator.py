# The implimentation of locator
import subprocess

def locate_string(string, path):
    print(subprocess.run(["grep", "-rl", string, path]).stdout)