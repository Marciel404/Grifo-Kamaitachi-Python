from discord.ext import commands
from checks.cargos import has_roles
from db.moderation import rmvNotify
from utils.loader import configData


class removeNotify(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["rmvNotify", "removeNTF"])
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"]
    )
    async def rmvnotificacao(self, ctx: commands.Context, idnotify: int):
        rmvNotify(idnotify)
        await ctx.reply("Notificação removida")


def setup(bot: commands.Bot):
    bot.add_cog(removeNotify(bot))