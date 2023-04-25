from pymongo import MongoClient
from funcs.derivadas import getdotenv

cluster = MongoClient(getdotenv("MongoKey"))
db = cluster[getdotenv("database_name")]
NaberiosAct = db["activityarte"]


def insert_atv_db(id, stamp):
    query = {"_id": id}
    insert = {"$set": {"_id": id, "last_arte": stamp}}
    NaberiosAct.update_one(query, insert, upsert=True)


def get_atv_db(id_array):
    query = {"_id": {"$in": id_array}}
    docs = NaberiosAct.find(query)
    return docs
