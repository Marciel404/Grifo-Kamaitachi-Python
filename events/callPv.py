import discord, asyncio

from discord.ext import commands
from utils.loader import configData


class events(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):

        if before.channel != after.channel:
            if after.channel is not None:
                if after.channel.id == configData['calls']['espera'] \
                        and member.guild.get_role(configData['roles']['ntb']) in member.roles \
                        or after.channel.id == configData['calls']['espera'] \
                        and member.guild.get_role(configData['roles']['nvl100']) in member.roles \
                        or after.channel.id == configData['calls']['espera'] \
                        and member.guild.get_role(configData['roles']["staff"]['staff1']) in member.roles \
                        or after.channel.id == configData['calls']['espera'] \
                        and member.guild.get_role(configData['roles']["staff"]['staff2']) in member.roles \
                        or after.channel.id == configData['calls']['espera'] \
                        and member.guild.get_role(configData['roles']['valak']) in member.roles \
                        or after.channel.id == configData['calls']['espera'] \
                        and member.guild.get_role(configData['roles']['artmes1']) in member.roles \
                        or after.channel.id == configData['calls']['espera'] \
                        and member.guild.get_role(configData['roles']['valak']) in member.roles \
                        or after.channel.id == configData['calls']['espera'] \
                        and member.guild_permissions.administrator:

                    overwrites = {

                        member.guild.default_role: discord.PermissionOverwrite(connect=False),

                        member: discord.PermissionOverwrite(connect=True),

                        discord.utils.get(member.guild.roles, name="BOTS"): discord.PermissionOverwrite(
                            connect=True,
                            view_channel=True,

                        )

                    }

                    call = await member.guild.create_voice_channel(
                        name=f'Pv [{member.name}]',
                        category=discord.utils.get(member.guild.categories, id=configData['categories']['callpv']),
                        overwrites=overwrites
                    )

                    await asyncio.sleep(1)

                    await member.move_to(call)

            if before.channel is not None \
                    and "Pv [" in before.channel.name \
                    and before.channel.members.__len__() == 0:

                await before.channel.delete()


def setup(bot: commands.Bot):
    bot.add_cog(events(bot))
