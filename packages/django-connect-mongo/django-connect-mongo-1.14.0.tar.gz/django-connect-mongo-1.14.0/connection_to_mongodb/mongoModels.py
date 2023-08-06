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

        if not hasattr(self, "create_thread"):
            self.create_thread = Process        

    def create(self, take_result=False):
        # kiem tra xem data da hop le hay chua
        self.validate_data()
        
        # thiet lap thoi gian tao
        self.data['create_at'] = datetime.datetime.utcnow()

        if take_result:
            return self.collection.insert_one(self.data)
        else:
            # tao trong thread, khong anh huong den cau lenh tiep theo
            self.create_thread(target=self.create_in_thread, args=(self.data,)).start()

    def create_in_thread(self, data):
        # khi ket noi voi mongodb o mot thread moi, ta can thiet lap mot client moi, neu 
        # khong se co the bi roi vao deadlock

        client = MongoClient(self.url)
        collection = client[self.db_name][self.collection_name]
        collection.insert_one(data)

    def validate_data(self):

        # xoa cac gia tri thua khong co trong khai bao fields
        for field in copy.deepcopy(self.data):
            if field not in self.fields:
                del self.data[field]

        # kiem tra xem cac gia tri nhap vao da dung type trong config hay chua
        for field in self.data:

            config = self.fields[field]

            if "type" in config:
                if not isinstance(self.data[field], config["type"]):

                    type_of_field = config["type"]
                    message_err = f"Value: '{self.data[field]}' in field '{field}' is incorrect for the type '{type_of_field}'"
                    
                    raise Exception(message_err)
                elif isinstance(self.data[field], bool) and config["type"] == int:
                    # truong hop dac biet, python tu dong chuyen bool sang int
                    # ta ngan truong hop nay

                    message_err = f"Can not convert {bool} to {int} in field {field}"
                    raise Exception(message_err)

        # gan cac gia tri default neu khong co trong self.data
        for field in self.fields:
            # lay config trong dinh nghia mongoModel
            config = self.fields[field]

            if "default" in config and field not in self.data:

                self.data[field] = config["default"]

                if "type" in config:

                    if not isinstance(config["default"], config["type"]):
                        # neu type cua gia tri default khong dung voi type trong config thi bao loi
                        type_of_field = config["type"]
                        value_of_default = config["default"]

                        message_err = f"Value of default: '{value_of_default}' in field '{field}' is incorrect for the type '{type_of_field}'"

                        raise Exception(message_err)
                    elif isinstance(self.data[field], bool) and config["type"] == int:
                        # truong hop dac biet, python tu dong chuyen tu bool sang int
                        # ta ngan truong hop nay lai

                        message_err = f"Can not convert {bool} to {int} in default value of field '{field}'"
                        raise Exception(message_err)
        
        # kiem tra xem co field nao required ma bi thieu khong
        for field in self.fields:

            # lay config trong dinh nghia mongoModel
            config = self.fields[field]

            if config.get("required", False) and field not in self.data:
                message_err = f"field {field} is required!"
                raise Exception(message_err)





if __name__ == "__main__":
    import urllib.parse

    url = "mongodb+srv://hieucao192:" + urllib.parse.quote("Caotrunghieu@192") + "@authenticationtest.6lh8w.mongodb.net/userSearch?retryWrites=true&w=majority"

    db_name = "websocket"

    class RoomNotificationModel(MongoBaseModel):
        fields = {
            "user_id_send": {
                "required": True,
                "default": 3,
                "type": int,
            },
            "user_id_receive": {
                "required": False
            },
            "room": {},
            "text": {},
            "is_seen": {
                "default": False,
                "type": bool,
            },
            "is_click": {
                "type": bool,
                "required": True
            },
            "is_new": { 
                "required": True,
                "default": True,
                "type": bool,
            },
        }

        url = url
        db_name = db_name
        collection_name = "roomNotifications"
        create_thread = threading.Thread


    RoomNotificationModel(room=1, text="hello", is_click=False, is_seen=False).create()