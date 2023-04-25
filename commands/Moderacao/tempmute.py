import discord

from datetime import datetime, timedelta
from discord.ext import commands
from checks.cargos import has_roles
from utils.loader import configData



class tempmute(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @commands.command(
        aliases=["mute", "mutetemp", "mutar"]
    )
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"],
        configData["roles"]["staff"]["ormenus"]
    )
    async def tempmute(self,
                       ctx: commands.Context,
                       member: discord.Member,
                       time: str,
                       *,
                       motivo: str = "Motivo não explicado"):

        if "d" in time.lower() or "dias" in time.lower():
            await member.timeout(
                datetime.utcnow() + timedelta(days=int(time.strip("dias"))),
                reason=motivo
            )
            await ctx.reply(f"{member.mention} mutado por {time.strip('dias')} dias")
        if "h" in time.lower() or "horas" in time.lower():
            await member.timeout(
                datetime.utcnow() + timedelta(hours=int(time.strip("horas"))),
                reason=motivo
            )
            await ctx.reply(f"{member.mention} mutado por {time.strip('horas')} horas")
        if "m" in time.lower() or "minutos" in time.lower():
            await member.timeout(
                datetime.utcnow() + timedelta(minutes=int(time.strip("minutos"))),
                reason=motivo
            )
            await ctx.reply(f"{member.mention} mutado por {time.strip('minutos')} minutos")


def setup(bot: commands.Bot):
    bot.add_cog(tempmute(bot))