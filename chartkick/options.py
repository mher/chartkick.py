from __future__ import absolute_import

import json
import logging


class Options(dict):
    def __init__(self, *args, **kwargs) :
        dict.__init__(self, *args, **kwargs)

    def load(self, filename):
        with open(filename) as jsonfile:
            options = json.loads(jsonfile.read())
            self.clear()
            for option in options:
                id = option.get('id', None)
                if id is None:
                    logging.warning("Missing chart 'id' in %s" % option)
                    continue
                self.update({id: option})
