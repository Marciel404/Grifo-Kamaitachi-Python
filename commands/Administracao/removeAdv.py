from discord.ext import commands
from checks.cargos import has_roles
from db.moderation import advs, rmvAdvertencia
from utils.loader import configData


class removeAdv(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["rmvAdvertencia", "removeAdv"])
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"]
    )
    async def rmvadv(self, ctx: commands.Context, idwarn: int):
        try:
            adv1 = ctx.guild.get_role(configData["roles"]["adv1"])
            adv2 = ctx.guild.get_role(configData["roles"]["adv2"])
            adv3 = ctx.guild.get_role(configData["roles"]["adv3"])

            member = ""

            for i in advs.find_one({"advertencias": {"$elemMatch": {"warn_id": idwarn}}}):
                member = ctx.guild.get_member(int(i["_id"]))
                break

            if adv3 in member.roles:
                rmvAdvertencia(idwarn)
                await ctx.reply("Advertencia removida")
                return await member.remove_roles(adv3)

            elif adv2 in member.roles:
                rmvAdvertencia(idwarn)
                await ctx.reply("Advertencia removida")
                return await member.remove_roles(adv2)

            elif adv1 in member.roles:
                rmvAdvertencia(idwarn)
                await ctx.reply("Advertencia removida")
                return await member.remove_roles(adv1)
        except:
            await ctx.reply("Advertencia não encontrada")


def setup(bot: commands.Bot):
    bot.add_cog(removeAdv(bot))
