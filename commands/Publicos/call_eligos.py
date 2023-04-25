from discord.ext import commands
from db.eligos import karaokeAct
from utils.loader import configData


class callEligos(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["callEligos", "call_eligos"])
    async def eligos(self, ctx: commands.Context):
        regs_in_karaoke = []
        regs_avaliables = []
        regs_avaliablesID = []

        for mem in ctx.guild.get_channel(configData["channels"]["karaoke_voice"]).members:
            if ctx.guild.get_role(configData["roles"]["equipe_karaoke"]) in mem.roles:
                regs_in_karaoke.append(mem.mention)

        for aval in karaokeAct.find({"available.state": True}):
            if ctx.guild.get_member(aval["_id"]):
                regs_avaliablesID.append(aval["_id"])
                regs_avaliables.append(ctx.guild.get_member(aval["_id"]).mention)

        if regs_avaliables:
            if regs_in_karaoke:
                for caps in ctx.guild.get_role(configData["roles"]["capitaes_karaoke"]).members:
                    try:
                        await caps.send(
                            f"Pediram ajuda no karaoke, porém já tem alguns eligos no karaoke {regs_in_karaoke}"
                        )
                    except:
                        pass

            await ctx.guild.get_channel(configData["channels"]["reinoEligos"]).send(
                f"Pediram ajuda no karaoke {regs_avaliables}"
            )

        elif regs_in_karaoke:

            for caps in ctx.guild.get_role(configData["roles"]["capitaes_karaoke"]).members:
                try:
                    await caps.send(
                        f"Pediram ajuda no Karaoke mas não tem ninguém disponivel, e tem alguns eligos no karaoke {regs_in_karaoke}"
                    )
                except:
                    pass

        else:

            for caps in ctx.guild.get_role(configData["roles"]["capitaes_karaoke"]).members:
                try:
                    await caps.send(
                        f"Pediram ajuda no Karaoke mas não tem ninguém disponivel"
                    )
                except:
                    pass

        await ctx.send("Já já vai vir alguém para ajudar")


def setup(bot: commands.Bot):
    bot.add_cog(callEligos(bot))
