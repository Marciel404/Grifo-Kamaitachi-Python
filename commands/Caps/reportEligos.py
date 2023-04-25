import discord
from datetime import datetime, timedelta
from checks.cargos import has_roles
from db.eligos import karaokeAct
from utils.loader import configData
from discord.ext import commands


class reportEligos(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @commands.command(name="reporteligos",
                      description="Exibe a contagem de pontos dos eligos",
                      guild_only=True)
    @has_roles(
        configData["roles"]["capitaes_karaoke"],
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"]
    )
    async def report(self, ctx: commands.Context, days: int = 30):

        if ctx.channel.id == configData["channels"]["listas_Karaoke"]:
            return await ctx.message.delete()

        await ctx.reply("Processando...")

        id_array = []
        for role in ctx.guild.roles:
            if role.id == configData["roles"]["equipe_karaoke"]:
                for organizer in role.members:
                    id_array.append(organizer.id)

        com_time = datetime.utcnow() - timedelta(days=days)
        docs_act = karaokeAct.find({"$and": [{"_id": {"$in": id_array}},{'activities.time': {"$gte": com_time.timestamp()}}]})

        regs_act = {}
        for doc in docs_act:
            tot = 0
            for act in doc["activities"]:

                if act["time"] >= com_time.timestamp():
                    if tot == 0:
                        tot = datetime.fromtimestamp(act["last"]) - datetime.fromtimestamp(act["inicial"])
                    else:
                        tot += datetime.fromtimestamp(act["last"]) - datetime.fromtimestamp(act["inicial"])
            regs_act[doc["_id"]] = {
                "time": convert(tot.total_seconds()),
            }

        emb = discord.Embed(title=f"Relatorio de {days} dias", colour=0x990f44).set_image(
            url="https://media.discordapp.net/attachments/750576681281912873/853674056691220530/20210612_154458_1.gif").set_thumbnail(
            url="https://media.baamboozle.com/uploads/images/291632/1619760072_114659_gif-url.gif").set_author(
            name=ctx.author.name,
            icon_url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png")
        emb.add_field(value="ㅤ", name="ㅤ")

        for regsAct in regs_act:
            m = ctx.guild.get_member(int(regsAct))
            emb.add_field(
                name=f"{m.name} {m.id}",
                value=regs_act[regsAct]["time"],
                inline=False
            )

        await ctx.author.send(embed=emb)
        await ctx.send("Enviado")


def setup(bot: commands.Bot):
    bot.add_cog(reportEligos(bot))


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    if hour == 0 and minutes < 20:
        return "Não está nem no tempo minimo"

    return "{} horas {} minutos {} segundos".format(int(hour), int(minutes), int(seconds))
