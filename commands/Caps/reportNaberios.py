from datetime import datetime, timedelta
from discord.ext import commands
from checks.cargos import has_roles
from db.naberios import get_atv_db, NaberiosAct
from utils.loader import configData

class reportNaberios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="reportNaberius",
        description="Envia o relatorio Naberius",
        guild_only=True
    )
    @has_roles(
        configData["roles"]["capitaes_arte"],
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"]
    )
    async def reportNaberius(self, ctx: commands.Context, dias: int = 30):
        await ctx.reply("Processando...")

        members_id = []
        all_mem = []

        for member in ctx.guild.get_role(configData["roles"]["equipe_arte"]).members:
            members_id.append(member.id)

        docs = get_atv_db(members_id)
        report_msg = "**Relatorio de atividade**"
        for doc in docs:
            all_mem.append((doc["_id"], doc["last_arte"]))

        memb = sorted(all_mem, key=lambda date: date[1])
        for tup in memb:
            date = datetime.fromtimestamp(tup[1]) - timedelta(hours=3)
            report_msg = report_msg + "\n" + date.strftime("%d/%m/%Y") + " --- " + f"<@{tup[0]}> {tup[0]}"
            if len(report_msg) >= 1800:
                await ctx.author.send(report_msg)
                report_msg = ""

        await ctx.author.send(report_msg)
        await ctx.send("Enviado!")

        com_time = datetime.utcnow() - timedelta(days=dias)

        qnt_msg = "**Quantidade de Desenhos**"

        desenhos_act = {}

        for qnt in NaberiosAct.find(
                {"$and": [{"_id": {"$in": members_id}}, {'activities.time': {"$gte": com_time.timestamp()}}]}
                    ):
            tot = 0
            for act in qnt["activities"]:

                if act["time"] >= com_time.timestamp():
                    tot += act["qnt"]

            desenhos_act[qnt["_id"]] = tot

        for i in sorted(desenhos_act, key=desenhos_act.get, reverse=True):

            qnt_msg += f"\n {ctx.guild.get_member(i).mention} --- {desenhos_act[i]} Desenhos"

            if len(qnt_msg) >= 1800:
                await ctx.author.send(qnt_msg)
                qnt_msg = ""

        await ctx.author.send(qnt_msg)


def setup(bot):
    bot.add_cog(reportNaberios(bot))
