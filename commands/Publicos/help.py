import discord

from discord.ext import commands
from funcs.derivadas import (
    getallComands,
    getModCommands,
    getEquipeEventosCommands,
    getStaffeCapsCommands,
    getStaffCommands,
    getPulicCommands,
    getCapsCommands,
    getEligosCommands,
    getCallPvCommands
)
from utils.loader import configData


class gerais(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context, tipo: str = "simples"):
        e = discord.Embed(title="Meus comandos", colour=discord.Colour.blurple())

        listcommands = ""

        if tipo.lower() == "detalhada" or tipo.lower() == "detalhado":
            listcommands += "Outras informações:\n....''[]'' opcional\n....''<>'' obrigatorio\n....'' | ''Um ou outro\n"
            tipo = "detalhada"

        if ctx.guild.get_role(configData["roles"]["staff"]["asmodeus"]) in ctx.author.roles \
                or ctx.guild.get_role(configData["roles"]["staff"]["astaroth"]) in ctx.author.roles \
                or ctx.author.guild_permissions.administrator:
            listcommands += getallComands(tipo.lower())

        if ctx.guild.get_role(configData["roles"]["staff"]["ormenus"]) in ctx.author.roles:

            if getModCommands(tipo.lower()) not in listcommands:
                listcommands += getModCommands(tipo.lower())
            if getStaffCommands(tipo.lower()) not in listcommands:
                listcommands += getStaffCommands(tipo.lower())
            if getStaffeCapsCommands(tipo.lower()) not in listcommands:
                listcommands += getStaffeCapsCommands(tipo.lower())

        if ctx.guild.get_role(configData["roles"]["staff"]["acacus"]) in ctx.author.roles:

            if getStaffCommands(tipo.lower()) not in listcommands:
                listcommands += getStaffCommands(tipo.lower())
            if getStaffeCapsCommands(tipo.lower()) not in listcommands:
                listcommands += getStaffeCapsCommands(tipo.lower())

        if ctx.guild.get_role(configData["roles"]["capitaes_karaoke"]) in ctx.author.roles \
                or ctx.guild.get_role(configData["roles"]["capitaes_poem"]) in ctx.author.roles \
                or ctx.guild.get_role(configData["roles"]["capitaes_arte"]) in ctx.author.roles \
                or ctx.guild.get_role(configData["roles"]["capitaes_evento"]) in ctx.author.roles:

            if getCapsCommands(tipo.lower()) not in listcommands:
                listcommands += getCapsCommands(tipo.lower())
            if getStaffeCapsCommands(tipo.lower()) not in listcommands:
                listcommands += getStaffeCapsCommands(tipo.lower())

        if ctx.guild.get_role(configData["roles"]["equipe_karaoke"]) in ctx.author.roles:

            if getEligosCommands(tipo.lower()) not in listcommands:
                listcommands += getEligosCommands(tipo.lower())

        if ctx.guild.get_role(configData["roles"]["capitaes_evento"]) in ctx.author.roles \
                or ctx.guild.get_role(configData["roles"]["equipe_evento"]) in ctx.author.roles:

            if getEquipeEventosCommands(tipo.lower()) not in listcommands:
                listcommands += getEquipeEventosCommands(tipo.lower())

        if ctx.guild.get_role(configData['roles']['ntb']) in ctx.author.roles \
                or ctx.guild.get_role(configData['roles']['nvl100']) in ctx.author.roles \
                or ctx.guild.get_role(configData['roles']["staff"]['staff1']) in ctx.author.roles \
                or ctx.guild.get_role(configData['roles']["staff"]['staff2']) in ctx.author.roles:

            if getCallPvCommands(tipo.lower()) not in listcommands:
                listcommands += getCallPvCommands(tipo.lower())

        listcommands += getPulicCommands(tipo.lower())

        e.description = listcommands
        await ctx.reply(embed=e)


def setup(bot: commands.Bot):
    bot.add_cog(gerais(bot))
