from datetime import datetime

import discord
from discord.ext import commands
from checks.cargos import has_roles
from db.eligos import karaokeAct
from utils.loader import configData


class offEligos(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_roles(
        configData["roles"]["equipe_karaoke"]
    )
    async def off(self, ctx: commands.Context):
        if ctx.channel.id != configData["channels"]["reinoEligos"]:
            return

        id_author = ctx.author.id
        query = {"_id": id_author}
        stamp_time = datetime.utcnow().timestamp()
        try:
            doc = karaokeAct.find_one(query)
            if doc and "available" in doc and doc["available"]["state"]:
                action_time = datetime.fromtimestamp(stamp_time) - datetime.fromtimestamp(doc["available"]["since"])
                insert = {"$set": {"_id": id_author, "last": stamp_time, "available": {"state": False, "since": None}},
                          "$push": {"time_available": {"When": stamp_time, "Total": action_time.total_seconds()}}}
                karaokeAct.update_many(query, insert)
                await ctx.send("Você agora está no modo ocupado")
            else:
                await ctx.send("Você precisa ficar disponivel primeiro para poder ficar no ocupado")
        except:
            print("Problema ao registrar na mongodb")


def setup(bot: commands.Bot):
    bot.add_cog(offEligos(bot))