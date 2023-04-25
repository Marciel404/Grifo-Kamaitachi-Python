import discord

from pymongo import MongoClient
from funcs.derivadas import getdotenv
from utils.loader import configData
from datetime import datetime, timedelta

cluster = MongoClient(getdotenv("MongoKey"))
db = cluster[getdotenv("database_name")]
advs = db["memberManegements"]
moddb = db["moderação"]


def RegAtivos(qnt):
    moddb.update_one(
        {"_id": "kamaiMod"}, {"$inc": {"regsAtivos": qnt}}, upsert=True
    )


def adcAdvertencia(
        author: discord.Member,
        member: discord.member,
        aprovador: discord.member,
        motivo: str,
        data: str,
        qnt
):
    moddb.update_one(
        {"_id": "kamaiMod"}, {"$inc": {"AdvsQnt": qnt}}, upsert=True
    )
    advs.update_one(
        {"_id": member.id},
        {"$push": {
            "advertencias": {
                "points": 1,
                "author": author.mention,
                "aprovador": aprovador.mention,
                "motivo": motivo,
                "data": data,
                "warn_id": moddb.find_one({"_id": "kamaiMod"})["AdvsQnt"]
            }
        }
        },
        upsert=True
    )


def rmvAdvertencia(
        warnid: int
):
    dt = datetime.now().utcnow() - timedelta(hours=3.0)

    advs.find_one_and_update({"advertencias": {"$elemMatch": {"warn_id": warnid}}},
                             {"$pull": {"advertencias": {"warn_id": warnid}},
                              "$set": {"UltimaRemoção": dt.strftime("%d/%m/%Y as %H:%M")}})


async def verifyAdvertencia(member: discord.Member):

    try:
        point = 0

        adv1 = member.guild.get_role(configData["roles"]["adv1"])
        adv2 = member.guild.get_role(configData["roles"]["adv2"])
        adv3 = member.guild.get_role(configData["roles"]["adv3"])

        for a1 in advs.find_one({"_id": member.id})["advertencias"]:
            point += a1["points"]

        if point == 1:
            await member.add_roles(adv1)
        if point == 2:
            await member.add_roles(adv1, adv2)
        if point == 3:
            await member.add_roles(adv1, adv2, adv3)
    except:
        pass


def adcNotify(
        author: discord.Member,
        member: discord.member,
        motivo: str,
        data: str,
        qnt
):
    moddb.update_one(
        {"_id": "kamaiMod"}, {"$inc": {"NtfsQnt": qnt}}, upsert=True
    )
    advs.update_one(
        {"_id": member.id},
        {"$push": {
            "Notifys": {
                "author": author.mention,
                "motivo": motivo,
                "data": data,
                "notify_id": moddb.find_one({"_id": "kamaiMod"})["NtfsQnt"]
            }
        }
        },
        upsert=True
    )


def rmvNotify(
        warnid: int
):
    dt = datetime.now().utcnow() - timedelta(hours=3.0)

    advs.find_one_and_update({"Notifys": {"$elemMatch": {"notify_id": warnid}}},
                             {"$pull": {"Notifys": {"notify_id": warnid}}})
