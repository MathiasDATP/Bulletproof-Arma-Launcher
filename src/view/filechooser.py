# Bulletproof Arma Launcher
# Copyright (C) 2016 Sascha Ebert
# Copyright (C) 2016 Lukasz Taczuk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from __future__ import unicode_literals

import os
import tkFileDialog
import tkMessageBox
import Tkinter

from kivy.logger import Logger
from kivy.uix.modalview import ModalView


class FileChooser():
    def __init__(self, path, on_success=None, on_canceled=None):
        self.path = path
        self.on_success = on_success
        self.on_canceled = on_canceled

        self.open()

    def _tk_open(self, _):
        root = Tkinter.Tk()
        root.withdraw()  # use to hide tkinter window

        while True:

            tempdir = tkFileDialog.askdirectory(
                parent=root,
                initialdir=self.path,
                title='')

            if not tempdir:
                Logger.info('FileChooser: User canceled the prompt')
                if self.on_canceled:
                    self.on_canceled()

                self.p.dismiss()
                return

            if os.sep != '/':  # askdirectory uses '/' as separator
                tempdir = tempdir.replace('/', os.sep)

            Logger.info('FileChooser: User selected {}'.format(tempdir))

            if not self.on_success:
                break

            # Call callback. If the callback returns something other than False
            # Show the message and get show the dir selection prompt again.
            message = self.on_success(tempdir)
            if message:
                Logger.error('FileChooser: {}'.format(message))
                tkMessageBox.showinfo('Error', message)

            else:
                break


        self.p.dismiss()

    def open(self):
        self.p = ModalView(size=(0, 0), size_hint=(None, None),
                           auto_dismiss=False, border=[0, 0, 0, 0])
        self.p.bind(on_open=self._tk_open)
        self.p.open()
