from discord import Invite
from discord.ext import commands
from checks.cargos import has_roles
from db.invites import invites
from utils.loader import configData


class remove_invite(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        description="Remove o cargo de um convite",
        aliases=["remove_invite", "rmv_invite"]
    )
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"]
    )
    async def rmv_invite_rewards(self, ctx: commands.Context, code: Invite):

        if invites.count_documents({"_id": code.code}) != 0:

            invites.delete_one({"_id": code.code})

            await ctx.reply(f"Prontinho :), {code.url} removido do banco de dados",
                            ephemeral=True)

        else:
            await ctx.reply(f"Erro: Não encontrei esse convite no meu banco de dados :(",
                            ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(remove_invite(bot))