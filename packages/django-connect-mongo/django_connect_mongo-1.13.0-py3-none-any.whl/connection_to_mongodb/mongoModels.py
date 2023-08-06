import threading, queue
from multiprocessing import Process, Queue
import datetime

from pymongo import MongoClient
import copy
from bson.objectid import ObjectId

import copy

class MongoBaseModel:
    def __init__(self, **kwargs):
        # user must defind self.db_name, self.collection_name, self.url, self.fields
        # default self.create_thread = Process

        client = MongoClient(self.url)
        self.collection = client[self.db_name][self.collection_name]

        self.data = copy.deepcopy(kwargs)
        self.create_thread = Process
        

    def create(self, take_result=False):
        self.validate_data()
        
        self.data['create_at'] = datetime.datetime.utcnow()

        if take_result:
            return self.collection.insert_one(self.data)
        else:
            self.create_thread(target=self.create_in_thread, args=(self.data,)).start()

    def create_in_thread(self, data):
        client = MongoClient(self.url)
        collection = client[self.db_name][self.collection_name]
        collection.insert_one(data)

    def validate_data(self):
        for field in copy.deepcopy(self.data):
            if field not in self.fields:
                del self.data[field]
        
        # kiem tra xem co field nao required ma bi thieu khong
        for field in self.fields:
            config = self.fields[field]
            if config.get("required", False) and field not in self.data:
                raise Exception(f"field {field} is required!")


