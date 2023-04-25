import discord
import os
from discord.ext import commands
from utils.loader import configData
from checks.cargos import has_roles
from classes.buttons import butonsListParticipar


class listaParticipantes(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @commands.command(
        name="lista_participantes",
        description="Envia os botões para adicionar os participantes",
        aliases=["lista_evento"]
    )
    @has_roles(
        configData["roles"]["staff"]["staff1"],
        configData["roles"]["staff"]["staff2"],
        configData["roles"]["equipe_evento"],
    )
    async def listaparticipantes(self, ctx: commands.Context):

        try:
            os.remove("listaEvento.txt")
        except:
            pass

        e = discord.Embed(title="Lista de participantes")

        await ctx.guild.get_channel(configData["channels"]["participantes_evento"]).send(
            embed=e,
            view=butonsListParticipar()
        )

        await ctx.send("Prontinho ;), Lista enviada")


def setup(bot: commands.Bot):
    bot.add_cog(listaParticipantes(bot))
