import discord

from discord.ext import commands
from utils.loader import configData
from checks.cargos import has_roles


class unban(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"]
    )
    async def unban(self, ctx: commands.Context, usuario: discord.User, motivo: str = "Motivo não informado"):
        await ctx.guild.unban(user=usuario, reason=motivo)

        await ctx.reply(f"{usuario.name} desbanido com sucesso")


def setup(bot: commands.Bot):
    bot.add_cog(unban(bot))