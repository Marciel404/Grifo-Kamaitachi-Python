import discord
from discord.ext import commands
from datetime import datetime, timedelta

from checks.cargos import has_roles
from utils.loader import configData


class memberDeleteMEssage(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        aliases=["mmd",
                 "messagemd",
                 "mMemberDelete",
                 "mMDelete"
                 ]
    )
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"],
        configData["roles"]["staff"]["ormenus"]
    )
    async def messageMemberDelete(
            self,
            ctx: commands.Context,
            member: discord.Member,
            tempo: str,
            *,
            reason: str = "Motivo não informado"):

        await ctx.reply("Começando a deletar as mensagens")

        count = 0

        if "d" in tempo.lower() or "dias" in tempo.lower():
            for i in set(ctx.guild.text_channels):
                for m in set(await i.history(limit=1000,
                                             before=datetime.utcnow(),
                                             after=datetime.utcnow() - timedelta(days=int(tempo.strip("dias")))
                                             ).flatten()):

                    if int(m.author.id) == int(member.id):
                        await m.delete(reason=reason)
                        count += 1

        if "h" in tempo.lower() or "horas" in tempo.lower():
            for i in set(ctx.guild.text_channels):
                for m in set(await i.history(limit=1000,
                                             before=datetime.utcnow(),
                                             after=datetime.utcnow() - timedelta(hours=int(tempo.strip("horas")))
                                             ).flatten()):

                    if int(m.author.id) == int(member.id):
                        await m.delete(reason=reason)
                        count += 1

        if "m" in tempo.lower() or "minutos" in tempo.lower():
            for i in set(ctx.guild.text_channels):
                for m in set(await i.history(limit=1000,
                                             before=datetime.utcnow(),
                                             after=datetime.utcnow() - timedelta(minutes=int(tempo.strip("horas")))
                                             ).flatten()):

                    if int(m.author.id) == int(member.id):
                        await m.delete(reason=reason)
                        count += 1

        await ctx.send(
            f"{ctx.author.mention}\nMensagens deletadas, foram deletadas {count} mensagens de {member.mention}")


def setup(bot: commands.Bot):
    bot.add_cog(memberDeleteMEssage(bot))
