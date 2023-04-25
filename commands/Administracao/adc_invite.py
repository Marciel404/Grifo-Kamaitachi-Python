from discord import Invite, Role
from discord.ext import commands
from datetime import datetime, timedelta
from checks.cargos import has_roles
from db.invites import insert_invite_reward
from utils.loader import configData


class adc_invite(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        description="Um membro ganha um cargo de acordo convite",
        aliases=["adicionar_invite", "adc_invite"]
    )
    @has_roles(
        configData["roles"]["staff"]["asmodeus"],
        configData["roles"]["staff"]["astaroth"]
    )
    async def adc_invite_rewards(self, ctx: commands.Context, code: Invite, cargo: Role):
        insert_invite_reward(
            ctx.author,
            datetime.now().utcnow().strftime("%d/%m/%Y as %H:%M") - timedelta(hours=3.0),
            code,
            cargo
        )

        await ctx.reply(f"Prontinho :), {cargo.mention} adicionado como recompensa pelo invite {code.url}")


def setup(bot: commands.Bot):
    bot.add_cog(adc_invite(bot))
