import os
import sys
import inspect

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../vendored"))

import urllib
from pymongo import MongoClient


def getDb():
    username = urllib.parse.quote_plus(os.environ['DB_USER'])
    password = urllib.parse.quote_plus(os.environ['DB_PASS'])
    mongo_uri = os.environ['MONGO_URI']
    client = MongoClient(mongo_uri % (username, password))
    db = client.get_database('jarbas')
    return db


def get_collection():
    return getDb().get_collection(os.environ['COLLECTION'])
