import discord

from pymongo import MongoClient
from funcs.derivadas import getdotenv

cluster = MongoClient(getdotenv("MongoKey"))
db = cluster[getdotenv("database_name")]
invites = db["invitesRewards"]


def insert_invite_reward(author: discord.Member, data, code: discord.Invite, role: discord.Role):
    invites.update_one(
        {"_id": code.code},
        {"$set": {
            "role": role.id,
            "author": author.id,
            "authorNameMoment": author.name,
            "data": data
        }
        },
        upsert=True
    )
