import asyncio

from discord.ext import tasks, commands

from db.eligos import db_temp_users, karaokeAct
from utils.loader import configData
from db.moderation import moddb, RegAtivos


class Tasks:

    def __init__(self, bot: commands.Bot):

        self.bot = bot
        super().__init__()

    @tasks.loop(minutes=5.0)
    async def regsChannelMod(self):

        try:
            regs = moddb.find_one({"_id": "kamaiMod"})["regsAtivos"]
            channel = self.bot.get_guild(configData["guild"]).get_channel(configData["channels"]["registrosAtivos"])

            if channel.name.replace("resgistros-ativos-", "") == regs:
                return

            try:
                await channel.edit(name=f"registros-ativos-{regs}")
            except:
                pass
        except:
            RegAtivos(0)

    @tasks.loop(minutes=5.0)
    async def updateKaraokeTime(self):

        opt = 0
        doc = 0
        try:
            if db_temp_users.all():
                for dic in db_temp_users:
                    try:
                        for act in karaokeAct.find_one({"_id": dic["_id"]})["activities"]:
                            if act["date"] == dic["date"]:
                                karaokeAct.find_one_and_update(
                                    {"activities": {
                                        "$elemMatch": {
                                            "date": dic["date"],
                                            "last": act["last"]
                                        }
                                    }
                                    },
                                    {"$set": {f"activities.{opt}.last": dic["last"]}}
                                )
                                doc += 1
                            else:
                                opt += 1
                        if doc == 0:
                            karaokeAct.update_one(
                                {"_id": dic["_id"]},
                                {"$push": {
                                    "activities": {
                                        "time": dic["last"],
                                        "date": dic["date"],
                                        "inicial": dic["last"],
                                        "last": dic["last"]
                                    }
                                }}, upsert=True)
                    except Exception as e:
                        karaokeAct.update_one(
                            {"_id": dic["_id"]},
                            {"$push": {
                                "activities": {
                                    "time": dic["last"],
                                    "date": dic["date"],
                                    "inicial": dic["last"],
                                    "last": dic["last"]
                                }
                            }
                            }, upsert=True)
                db_temp_users.truncate()
        except:
            print("Erro ao salvar dbMongo")
