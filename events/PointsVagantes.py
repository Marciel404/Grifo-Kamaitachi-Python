import discord

from utils.loader import configData
from discord.ext import commands
from datetime import datetime, timedelta
from db.vagantes import insert_atv_db, VagantesAct


class PointsVagantes(commands.Cog):

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        opt = 0
        doc = 0
        points = 1

        if configData["channels"]["poem_post"] == message.channel.id:
            if message.guild.get_role(configData["roles"]["equipe_poem"]) in message.author.roles:
                now = datetime.utcnow().timestamp()
                insert_atv_db(message.author.id, now)
                try:
                    VagantesAct.find_one({"_id": message.author.id})["activities"]
                    date = datetime.utcnow() - timedelta(hours=3)
                    for act in VagantesAct.find_one({"_id": message.author.id})["activities"]:
                        if act["date"] == date.strftime("%d %m %Y"):
                            VagantesAct.find_one_and_update(
                                {"activities": {
                                    "$elemMatch": {"date": date.strftime("%d %m %Y"), "qnt": act["qnt"]}}},
                                {"$inc": {f"activities.{opt}.qnt": points}

                                 }
                            )
                            doc += 1
                        else:
                            opt += 1
                    if doc == 0:
                        VagantesAct.update_one({"_id": message.author.id}, {"$push": {
                            "activities": {
                                "time": date.timestamp(),
                                "date": date.strftime("%d %m %Y"),
                                "qnt": points
                            }
                        }}, upsert=True)
                except Exception as e:
                    date = datetime.utcnow() - timedelta(hours=3)
                    VagantesAct.update_one(
                        {"_id": message.author.id},
                        {"$push": {
                            "activities": {
                                "time": date.timestamp(),
                                "date": date.strftime("%d %m %Y"),
                                "qnt": points
                            }
                        }
                        }, upsert=True)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        opt = 0
        doc = 0
        points = 1

        if configData["channels"]["poem_post"] == message.channel.id:
            if message.guild.get_role(configData["roles"]["equipe_poem"]) in message.author.roles:
                now = datetime.utcnow().timestamp()
                insert_atv_db(message.author.id, now)
                try:
                    VagantesAct.find_one({"_id": message.author.id})["activities"]
                    date = datetime.utcnow() - timedelta(hours=3)
                    for act in VagantesAct.find_one({"_id": message.author.id})["activities"]:
                        if act["date"] == date.strftime("%d %m %Y"):
                            VagantesAct.find_one_and_update(
                                {"activities": {
                                    "$elemMatch": {"date": date.strftime("%d %m %Y"), "qnt": act["qnt"]}}},
                                {"$inc": {f"activities.{opt}.qnt": - points}

                                 }
                            )
                            doc += 1
                        else:
                            opt += 1
                    if doc == 0:
                        VagantesAct.update_one({"_id": message.author.id}, {"$push": {
                            "activities": {
                                "time": date.timestamp(),
                                "date": date.strftime("%d %m %Y"),
                                "qnt": - points
                            }
                        }}, upsert=True)
                except Exception as e:
                    date = datetime.utcnow() - timedelta(hours=3)
                    VagantesAct.update_one(
                        {"_id": message.author.id},
                        {"$push": {
                            "activities": {
                                "time": date.timestamp(),
                                "date": date.strftime("%d %m %Y"),
                                "qnt": - points
                            }
                        }
                        }, upsert=True)


def setup(bot):
    bot.add_cog(PointsVagantes(bot))
