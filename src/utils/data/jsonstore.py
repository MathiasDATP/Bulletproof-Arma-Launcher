# Tactical Battlefield Installer/Updater/Launcher
# Copyright (C) 2015 TacBF Installer Team.
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

import json

from kivy.logger import Logger


class JsonStore(object):
    """saves models to a json file"""
    def __init__(self, filepath):
        super(JsonStore, self).__init__()
        self.filepath = filepath

    def save(self, model):


        # build new dict with items which have persist set not to False
        dict_to_save = {}

        for field in model.fields:
            if 'persist' in field and field['persist'] == False:
                continue
            else:
                dict_to_save[field['name']] = model.get(field['name'])


        string = json.dumps(dict_to_save, sort_keys=True,
                            indent=4, separators=(',', ': '))

        Logger.info('JsonStore: Saving model: {} to {} | {}'.format(
                    model, self.filepath, string))

        with open(self.filepath, "w") as text_file:
            text_file.write(string)

    def load(self, model, update=True):

        with open(self.filepath, "r") as text_file:
            data = json.load(text_file)
            if update:
                model.data.update(data)
            else:
                model.data = data

        nice_model_data = json.dumps(model.data, sort_keys=True,
                            indent=4, separators=(',', ': '))
                            
        Logger.info('JsonStore: Loaded model: {} from {} | {} '.format(
                    model, self.filepath, nice_model_data))

        return model
