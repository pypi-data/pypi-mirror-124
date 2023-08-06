#!/usr/bin/env python3
"""
Module TEXTFILE -- UI File-Aware Text Control Helper
Sub-Package UI of Package PLIB3 -- Python UI Framework
Copyright (C) 2008-2020 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information
"""

import os

from plib.ui.defs import *


class PTextFile(object):
    """Make a text edit control file-aware.
    """
    
    untitled = object()
    
    def __init__(self, app, control):
        self.control = control  # should normally be a PEditControl
        self.app = app
        self.main_window = app.main_window
        self.base_title = app.main_title
        self.file_path = os.curdir
        self.file_filter = "*.txt"
        self.filename = None
        self.dirty = False
        
        # So we can keep track of "dirty" state
        control.setup_notify(SIGNAL_TEXTMODCHANGED, self.editor_changed)
    
    @property
    def filesize(self):
        return len(self.control.edit_text)
    
    def set_filename(self, filename):
        self.filename = filename
        if filename:
            self.main_window.set_caption("{} - {}".format(
                self.base_title,
                "<Untitled>" if filename is self.untitled else filename
            ))
        else:
            self.main_window.set_caption(self.base_title)
    
    def new_file(self):
        self.close_file()
        self.set_filename(self.untitled)
    
    def open_data(self, filename):
        with open(filename, 'r') as f:
            data = f.read()
        self.control.edit_text = data
        self.dirty = False
    
    def open_file(self):
        filename = self.app.file_dialog.open_filename(self.file_path, self.file_filter)
        if filename:
            self.open_data(filename)
            self.set_filename(filename)
            return True
        return False
    
    def editor_changed(self, changed):
        self.dirty = changed
    
    def save_data(self, filename):
        data = self.control.edit_text
        with open(filename, 'w') as f:
            f.write(data)
        self.dirty = False
    
    def save_file_as(self):
        filename = self.app.file_dialog.save_filename(self.file_path, self.file_filter)
        if filename:
            self.save_data(filename)
            self.set_filename(filename)
            return True
        return False
    
    def save_file(self):
        if (not self.filename) or (self.filename is self.untitled):
            return self.save_file_as()
        else:
            self.save_data(self.filename)
            return True
    
    def close_file(self):
        # Calling application must make sure data is saved first
        self.control.clear_edit()
        self.set_filename(None)
        self.dirty = False
