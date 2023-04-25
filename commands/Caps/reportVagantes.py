from datetime import datetime, timedelta
from discord.ext import commands
from checks.cargos import has_roles
from db.vagantes import get_atv_db, VagantesAct
from utils.loader import configData


class reportVagantes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="reportVagantes",
        description="Envia o relatorio Vagantes",
        guild_only=True,
    )
    @has_roles(
        configData["roles"]["capitaes_poem"],
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"]
    )
    async def _report(self, ctx: commands.Context, dias: int = 30):
        await ctx.reply("Processando...")

        members_id = []
        all_mem = []

        for member in ctx.guild.get_role(configData["roles"]["equipe_arte"]).members:
            members_id.append(member.id)

        docs = get_atv_db(members_id)
        report_msg = "**Relatorio de atividade**"
        for doc in docs:
            all_mem.append((doc["_id"], doc["last_poem"]))

        for tup in sorted(all_mem, key=lambda date: date[1]):
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

        for qnt in VagantesAct.find(
                {"$and": [{"_id": {"$in": members_id}}, {'activities.time': {"$gte": com_time.timestamp()}}]}
        ):
            tot = 0
            for act in qnt["activities"]:

                if act["time"] >= com_time.timestamp():
                    tot += act["qnt"]

            desenhos_act[qnt["_id"]] = tot

        for i in sorted(desenhos_act, key=desenhos_act.get, reverse=True):

            qnt_msg += f"\n {ctx.guild.get_member(i).mention} --- {desenhos_act[i]} Poemas"

            if len(qnt_msg) >= 1800:
                await ctx.author.send(qnt_msg)
                qnt_msg = ""

        await ctx.author.send(qnt_msg)


def setup(bot):
    bot.add_cog(reportVagantes(bot))
