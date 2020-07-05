"""
    Author: Sujayyendhiren RS
    Description: Simple wrapper class around simplkv to avoid having to encode/decode 
                 and to automatically convert lists and dictionaries ready to be
                 consumed.
"""

import os
import json
import traceback

try:
    from simplekv.fs import FilesystemStore
except:
    print(traceback.format_exc())


class StorageWrapper():

    __STORAGE__ = "store"

    def __init__(self, cachename):

        storage = StorageWrapper.__STORAGE__

        if not os.path.exists(f"{storage}"):
            os.system(f"mkdir -p {storage}")

        self.store = FilesystemStore(f"{storage}/{cachename}")

    def add_kv(self, key, value):
        if type(value) is str:
            self.store.put(key, value.encode('utf-8'))

        elif type(value) is dict or type(value) is list:
            self.store.put(key, json.dumps(value).encode('utf-8'))

    def update_kv(self, key, value):
        pass

    def get_kv(self, key):

        try:
            value = self.store.get(key) 
            strvalue = value.decode('utf-8') 

            if (strvalue.startswith("{") and strvalue.endswith("}")) or \
                    (strvalue.startswith("[") and strvalue.endswith("]")):
                return key, json.loads(strvalue)

            return key, strvalue 

        except:
            return key, None
