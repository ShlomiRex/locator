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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import time
import threading
import os
import queue


# Input: filenames from grep command
# Output: None. Change GUI.
class WorkerThread(threading.Thread):
    def __init__(self, input_q, listbox, finishedSearchingEvent, maxRows=50):
        self.input_q, self.listbox, self.maxRows, self.finishedSearchingEvent = input_q, listbox, maxRows, finishedSearchingEvent
        self.stoprequest = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        i = 1
        # While GREP command is still running, keep reading!
        while True:
            try:
                if self.finishedSearchingEvent.isSet() and self.input_q.empty():
                    print("GUI Thread stopped - GREP signal")
                    break
                else:
                    print("No GREP signal")
                # Maximum GUI elements!
                if i == self.maxRows:
                    print("GUI Thread stopped due to max GUI rows reached")
                    break
                # If there is nothing in queue, after X seconds, skip. This allows for 'isAlive' check, if we need to gracefuly exit.
                filename = self.input_q.get(True, 0.5)
                label = Gtk.Label(filename)
                self.listbox.add(label)
                label.show_all()
                i = i + 1
            except queue.Empty:
                continue
        
    
    # Called externally. Gracefuly stop the task.
    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)

def windowThread(listbox):    
    builder = Gtk.Builder()
    builder.add_from_file("SearchWindow.glade")
    window = builder.get_object("SearchWindow")
    box_outer = builder.get_object("GtkBox")

    listbox = Gtk.ListBox()
    #Do not delete these comments, it may be useful in the future

    # def sort_func(row_1, row_2, data, notify_destroy):
    #     return row_1.data.lower() > row_2.data.lower()

    # def filter_func(row, data, notify_destroy):
    #     return False if row.data == 'Fail' else True

    # listbox.set_sort_func(sort_func, None, False)
    # listbox.set_filter_func(filter_func, None, False)

    box_outer.pack_start(listbox, True, True, 0)
    #builder.connect_signals(Handler())
    #window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()

def show(input_q, finishedSearchingEvent):
    listbox = None
    # Start window thread
    threading.Thread(target=windowThread, args=(listbox)).start()
    
    # Start thread
    thread = WorkerThread(input_q, listbox, finishedSearchingEvent).start()
