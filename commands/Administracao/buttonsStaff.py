from discord.ext import commands
from utils.loader import configData
from checks.cargos import has_roles
from classes.buttons import buttonsStaff


class buttonsRegStaff(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"]
    )
    async def buttonsStaff(self, ctx: commands.Context):
        await ctx.send(view=buttonsStaff())
        await ctx.message.delete()


def setup(bot: commands.Bot):
    bot.add_cog(buttonsRegStaff(bot))
