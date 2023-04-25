import discord
from discord.ext import commands
from checks.cargos import has_roles
from utils.loader import configData


class say(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_roles(
        configData["roles"]["staff"]["staff1"],
        configData["roles"]["staff"]["staff2"],
    )
    async def say(self, ctx: commands.Context, canal: discord.TextChannel, *, msg: str):
        await canal.send(msg)

        await ctx.reply(content=f"Mensagem enviada no canal {canal.mention}")


def setup(bot: commands.Bot):
    bot.add_cog(say(bot))