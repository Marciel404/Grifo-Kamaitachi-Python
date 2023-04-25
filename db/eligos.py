from pymongo import MongoClient
from tinydb import TinyDB
from funcs.derivadas import getdotenv

db_temp_users = TinyDB('./temporary db/ActivityKaraoke.json')

cluster = MongoClient(getdotenv("MongoKey"))
db = cluster[getdotenv("database_name")]
karaokeAct = db["karaokeAct"]
