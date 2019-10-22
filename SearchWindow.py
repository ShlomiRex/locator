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
    def __init__(self, input_q):
        self.input_q = input_q
        self.stoprequest = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        while not self.stoprequest.isSet():
            try:
                # If there is nothing in queue, after X seconds, skip.
                filenames = self.input_q.get(True, 0.2)
                print(filenames)
                # self.output_q.put((self.name, dirname, filenames))
            except Queue.Empty:
                continue
    
    # Called externally. Gracefuly stop the task.
    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)


def show(input_q):
    builder = Gtk.Builder()
    builder.add_from_file("SearchWindow.glade")
    window = builder.get_object("SearchWindow")
    box_outer = builder.get_object("GtkBox")

    listbox_2 = Gtk.ListBox()
    items = 'This is a sorted ListBox Fail'.split()


    #Do not delete these comments, it may be useful in the future

    # def sort_func(row_1, row_2, data, notify_destroy):
    #     return row_1.data.lower() > row_2.data.lower()

    # def filter_func(row, data, notify_destroy):
    #     return False if row.data == 'Fail' else True

    # listbox_2.set_sort_func(sort_func, None, False)
    # listbox_2.set_filter_func(filter_func, None, False)


    for item in items:
        listbox_2.add(Gtk.Label(item))

    box_outer.pack_start(listbox_2, True, True, 0)
    #builder.connect_signals(Handler())
    #window.connect("destroy", Gtk.main_quit)
    window.show_all()

    WorkerThread(input_q).start()

    Gtk.main()
