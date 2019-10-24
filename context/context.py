import os
import sys
import inspect

sys.path.insert(0, './vendored')

import urllib
from pymongo import MongoClient


def getDb():
    username = urllib.parse.quote_plus(os.environ['DB_USER'])
    password = urllib.parse.quote_plus(os.environ['DB_PASS'])
    mongo_uri = os.environ['MONGO_URI']
    client = MongoClient(mongo_uri % (username, password))
    db = client.get_database('jarbas')
    return db


def get_ct_collection():
    return getDb().get_collection(os.environ['CT_COLLECTION'])

def get_ceic_collection():
    return getDb().get_collection(os.environ['CEIC_COLLECTION'])

def get_log_collection():
    return getDb().get_collection(os.environ['LOG_COLLECTION'])

