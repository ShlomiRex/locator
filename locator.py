'''
MIT License

Copyright (c) 2019 Shlomi Domnenko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# The implimentation of locator
import subprocess

import threading
import time
import pipes


class Searcher(threading.Thread):
    def __init__(self, string, path, spinner):
        self.string, self.path, self.spinner = string, path, spinner

        threading.Thread.__init__(self)
    
    def run(self):
        #p = subprocess.Popen(["grep", "-rln", self.string, self.path],  shell=False, stdout=open("out.txt", "w"), stderr=open("err.txt", "w"))
        cmd = "grep -rn {} {}".format(self.string, self.path)
        self.p = subprocess.run(cmd,  shell=True)
        self.spinner.stop()
    
    def stop():
        self.p.kill()

def locate_string(string, path, spinner = None):
    myclass = Searcher(string, path, spinner)
    myclass.start()
    return myclass




if __name__ == '__main__':
    myclass = Searcher("Base", "/home/shlomi/Desktop/locator")
    myclass.start()
    myclass.join()