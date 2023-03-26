import pymongo
import os

from webapi.dbclasses.dbmongo import DbMongo

class OwnerCollection:

    def __init__(self):
        self.client, self.db = DbMongo.getDB()
        self.collection = "webapi_duenio"
    
    def getOne(self, id):
        collection = self.db[self.collection]
        return collection.find_one({"id_nacional": id})