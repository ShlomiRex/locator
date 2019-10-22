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

import locator
import time
import queue
import SearchWindow

filenames_q = None

class Handler:
    def onSearch(self, button):
        search_str = builder.get_object("search_string").get_text()
        path_str = builder.get_object("folder_path").get_text()

        stop_button.set_visible(True)
        spinner.set_visible(True)
        spinner.start()
        
        grep_output = queue.Queue()
        self.searcher = locator.locate_string(search_str, path_str, self.postSearch, grep_output)
        #searchWindow.show(filenames_q)
    
    def postSearch(self):
        print("Finished searching")
        stop_button.set_visible(False)
        spinner.stop()
        spinner.set_visible(False)
        

    def on_folder_clicked(self, button):
        dialog = Gtk.FileChooserDialog("Please choose a folder", window,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        #dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            folder_path = dialog.get_filename()
            print("Select clicked")
            print("Folder selected: " + folder_path)
            builder.get_object("folder_path").set_text(folder_path)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
    
    def stop_searching(self, button):
        print("onClicked_stopSearching")
        stop_button.set_visible(False)
        spinner.stop()
        spinner.set_visible(False)
        
# Build PyGObject from glade
builder = Gtk.Builder()
builder.add_from_file("MainWindow.glade")
builder.connect_signals(Handler())

# Main window
window = builder.get_object("MainWindow")
window.connect("destroy", Gtk.main_quit)
window.show()

spinner = builder.get_object("spinner")
stop_button = builder.get_object("btn_stop_search")


Gtk.main()