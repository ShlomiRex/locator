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
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)

# Input: filenames from grep command, listbox to change the GUI, an event when GREP command finished
class WorkerThread(threading.Thread):
    def __init__(self, input_q, listbox, finishedSearchingEvent, maxRows=50):
        self.input_q, self.listbox, self.maxRows, self.finishedSearchingEvent = input_q, listbox, maxRows, finishedSearchingEvent
        threading.Thread.__init__(self, name="WorkerThread")

    def run(self):
        logging.debug("WorkerThread started")
        # While GREP command is still running, keep reading!
        while True:
            try:
                # If there is nothing in queue, after X seconds, skip. This allows for 'isAlive' check, if we need to gracefuly exit.
                filename = self.input_q.get(block=True, timeout=None)
                logging.debug(filename)
                label = Gtk.Label(filename)
                self.listbox.add(label)
                label.show_all()
            except queue.Empty:
                if self.finishedSearchingEvent.isSet() :
                    break
        logging.debug("WorkerThread finished")

class WindowThread(threading.Thread):
    def __init__(self, input_q, finishedSearchingEvent):
        self.input_q, self.finishedSearchingEvent = input_q, finishedSearchingEvent
        threading.Thread.__init__(self, name="SearchWindowThread")
    def run(self):
        logging.debug("Initializing window")
        builder = Gtk.Builder()
        builder.add_from_file("SearchWindow.glade")
        window = builder.get_object("SearchWindow")
        box_outer = builder.get_object("GtkBox")

        listbox = Gtk.ListBox()
        box_outer.pack_start(listbox, True, True, 0)
        window.connect("destroy", Gtk.main_quit)
        window.show_all()

        self.thread = WorkerThread(self.input_q, listbox, self.finishedSearchingEvent, maxRows=100)
        self.thread.start()

        logging.debug("Running window loop")
        Gtk.main()
    def isWorkerThreadAlive(self):
        return self.thread.isAlive()