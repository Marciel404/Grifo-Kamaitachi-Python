import discord
from discord.ext import commands
from tinydb import table

from db.eligos import karaokeAct, db_temp_users
from utils.loader import configData
from datetime import datetime, timedelta


class eligosXpCall(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self,
                                    member: discord.Member,
                                    old_state: discord.VoiceState,
                                    new_state: discord.VoiceState):

        if old_state.self_mute != new_state.self_mute \
                and member.guild.get_role(configData["roles"]["equipe_karaoke"]) in member.roles \
                and new_state.channel == member.guild.get_channel(configData["channels"]["karaoke_voice"]):

            if not karaokeAct.find_one({"_id": member.id})["available"]["state"] \
                    or new_state.channel.members.__len__() < 3:
                return

            for msg in await member.guild.get_channel(configData["channels"]["listas_Karaoke"]) \
                    .history(limit=1,
                             oldest_first=False
                             ).flatten():
                if msg.author != member:
                    return

            try:
                karaokeAct.find_one({"_id": member.id})["activities"]
                date = datetime.utcnow() - timedelta(hours=3)
                try:
                    if db_temp_users.contains(doc_id=member.id):
                        doc = db_temp_users.get(doc_id=member.id)
                        doc["last"] = date.timestamp()
                        db_temp_users.update(doc, doc_ids=[member.id])
                    else:
                        try:
                            insert = {"_id": member.id,
                                      "date": date.strftime("%d %m %Y"),
                                      "last": date.timestamp()
                                      }
                            db_temp_users.insert(table.Document(insert, doc_id=member.id))
                        except Exception as e:
                            print("Um erro ocorreu ao registrar na db interna " + e)
                except Exception as e:
                    print("Um erro ocorreu ao registrar atividade " + e)

            except Exception as e:
                date = datetime.utcnow() - timedelta(hours=3)
                karaokeAct.update_one(
                    {"_id": member.id},
                    {"$push": {
                        "activities": {
                            "time": date.timestamp(),
                            "date": date.strftime("%d %m %Y"),
                            "inicial": date.timestamp(),
                            "last": 0
                        }
                    }
                    }, upsert=True)


def setup(bot: commands.Bot):
    bot.add_cog(eligosXpCall(bot))
