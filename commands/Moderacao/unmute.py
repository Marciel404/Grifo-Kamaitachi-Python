import discord

from discord.ext import commands
from checks.cargos import has_roles
from utils.loader import configData


class invitesRewards(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @commands.command(
        aliases=["desmutar"]
    )
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"],
        configData["roles"]["staff"]["ormenus"]
    )
    async def unmute(self,
                     ctx: commands.Context,
                     member: discord.Member,
                     reason: str = "Motivo não justificado"
                     ):

        if member.timed_out:
            await member.remove_timeout(reason=reason)
            await ctx.reply(f"{member.mention} desmutado com sucesso")
        else:
            await ctx.reply(f"{member.mention} não está mutado")


def setup(bot: commands.Bot):
    bot.add_cog(invitesRewards(bot))