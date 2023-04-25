import discord
from discord.ext import commands
from checks.cargos import has_roles
from db.eligos import karaokeAct
from utils.loader import configData
from datetime import datetime


class onEligos(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_roles(
        configData["roles"]["equipe_karaoke"]
    )
    async def on(self, ctx: commands.Context):
        if ctx.channel.id != configData["channels"]["reinoEligos"]:
            return

        query = {"_id": ctx.author.id}
        stamp_time = datetime.utcnow()

        def days_hours_minutes(td):
            return td.days, td.seconds // 3600, (td.seconds // 60) % 60

        try:
            doc = karaokeAct.find_one(query)
            if doc and "available" in doc and doc["available"]["state"]:
                date_started = datetime.utcnow() - datetime.fromtimestamp(doc["available"]["since"])
                date_days, date_hours, date_minutes = days_hours_minutes(date_started)
                await ctx.reply(f"Você já esta disponivel, a {date_days}d {date_hours}h {date_minutes}m")
            else:
                insert = {"$set": {"_id": ctx.author.id, "available": {"state": True, "since": stamp_time.timestamp()}}}
                karaokeAct.update_many(query, insert, upsert=True)
                await ctx.reply("Você agora esta disponivel")
        except:
            print('Problemas ao registrar na mongodb')


def setup(bot: commands.Bot):
    bot.add_cog(onEligos(bot))