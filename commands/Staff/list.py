import discord

from discord.ext import commands
from checks.cargos import has_roles
from db.moderation import advs
from utils.loader import configData


class list(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"],
        configData["roles"]["staff"]["staff1"],
        configData["roles"]["staff"]["staff2"]
    )
    async def list(self, ctx: commands.Context, member: discord.Member):
        e = discord.Embed(title=f"Advertencias de {member.name}")
        v = 0
        try:
            for a1 in advs.find_one({"_id": member.id})["advertencias"]:
                e.add_field(
                    name=f'Advertencia id: ({a1["warn_id"]})',
                    value="Autor: {} \nAprovado por: {} \nMotivo: {} \nData: {}".format(
                        a1["author"], a1["aprovador"], a1["motivo"], a1["data"]
                    ),
                    inline=False
                )
                v += 1
            if v == 0:
                var = advs.find_one({"_id": "44"})["UltimaRemoção"]

            try:
                if advs.find_one({"_id": member.id})["UltimaRemoção"] is not None:
                    e.set_footer(text=f'Ultima remoção: {advs.find_one({"_id": member.id})["UltimaRemoção"]}')
            except:
                pass
            await ctx.reply(embed=e)
        except Exception as err:
            s = ""
            try:
                if advs.find_one({"_id": member.id})["UltimaRemoção"] is not None:
                    s = f'ultima remoção: {advs.find_one({"_id": member.id})["UltimaRemoção"]}'
            except:
                pass
            await ctx.reply(f"Esse membro não tem Advertencias no momento\n{s}")


def setup(bot: commands.Bot):
    bot.add_cog(list(bot))