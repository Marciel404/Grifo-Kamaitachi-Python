import discord
from discord.ext import commands
from checks.cargos import has_roles
from db.moderation import advs
from utils.loader import configData


class listNotify(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"],
        configData["roles"]["staff"]["staff1"],
        configData["roles"]["staff"]["staff2"]
    )
    async def listNotify(self, ctx: commands.Context, member: discord.Member):

        e = discord.Embed(title=f"Notificações de {member.name}")
        v = 0
        try:
            for a1 in advs.find_one({"_id": member.id})["Notifys"]:
                e.add_field(
                    name=f'Notificação id: ({a1["notify_id"]})',
                    value="Autor: {} \nMotivo: {} \nData: {}".format(
                        a1["author"], a1["motivo"], a1["data"]
                    ),
                    inline=False
                )
                v += 1
            if v == 0:
                var = advs.find_one({"_id": "44"})["UltimaRemoção"]

            await ctx.reply(embed=e)
        except Exception as err:

            await ctx.reply(f"Esse membro não tem notificações no momento")


def setup(bot: commands.Bot):
    bot.add_cog(listNotify(bot))
