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


# output_q - Save filenames in this container.
class Searcher(threading.Thread):
    def __init__(self, string, path, callback, output_q):
        self.string, self.path, self.callback, self.output_q = string, path, callback, output_q

        threading.Thread.__init__(self)
    
    def run(self):
        print("Searching...")
        cmd = "grep -rnIh {} {}".format(self.string, self.path)
        # Create process in diffirent thread.
        p = subprocess.Popen(cmd, stdout= subprocess.PIPE, shell=True)
        # Keep reading output of p. If finished, check if p is dead. If not, keep reading, if yes, terminate.
        while True:
            line = p.stdout.readline()
            if not line or p.poll() != None:
                break
            line_str = line.rstrip().decode("utf-8")  # Turn bytes into formatted string line.
            print(line_str)
            # Queue the filename. (Output)
            self.output_q.put(line_str)

        print("Shell command finished")
        # Finished running, call callback
        self.callback()