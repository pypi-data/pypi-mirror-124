import threading, queue
from multiprocessing import Process, Queue
import datetime

from pymongo import MongoClient
import copy
from bson.objectid import ObjectId

import copy


def create_connection_to_mongo(db_name, collection_name, url):
    client = MongoClient(url)
    return client['db_name']['collection_name']
    # local_func = locals()
    # exec(f"connected = client.{db_name}.{collection_name}", globals(), local_func)
    # connected = local_func["connected"]
    # return connected


class MongoBaseModel:
    def __init__(self, **kwargs):
        # user must defind self.db_name, self.collection_name, self.url, self.fields
        # default self.create_thread = Process

        self.collection = create_connection_to_mongo(self.db_name, self.collection_name, self.url)

        self.data = copy.deepcopy(kwargs)
        self.create_thread = Process
        
        self.validate_data()

    def create(self, take_result=False):
        self.data['create_at'] = datetime.datetime.utcnow()

        if take_result:
            return self.collection.insert_one(self.data)
        else:
            self.create_thread(target=self.create_in_thread, args=(self.data,)).start()

    def create_in_thread(self, data):
        create_connection_to_mongo(self.db_name, self.collection_name, self.url).insert_one(data)

    def validate_data(self):
        for field in copy.deepcopy(self.data):
            if field not in self.fields:
                del self.data[field]
        
        # kiem tra xem co field nao required ma bi thieu khong
        for field in self.fields:
            config = self.fields[field]
            if config['required'] and field not in self.data:
                raise Exception(f"field {field} is required!")


