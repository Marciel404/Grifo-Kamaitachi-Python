import discord
from discord.ext import commands
from checks.cargos import has_roles
from utils.loader import configData


class clear(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"],
        configData["roles"]["staff"]["ormenus"]
    )
    async def clear(self, ctx: commands.Context, qnt: int):

        if qnt > 100:
            qnt = 100

        mc = await ctx.channel.purge(limit=qnt)

        await ctx.reply(f"O canal teve {mc.__len__()} mensagens apagadas")


def setup(bot: commands.Bot):
    bot.add_cog(clear(bot))