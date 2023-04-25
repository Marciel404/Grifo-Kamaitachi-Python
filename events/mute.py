import discord
from discord.ext import commands
from utils.loader import configData


class muteEvents(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, oldstate: discord.VoiceState,
                                    newstate: discord.VoiceState):

        if newstate.mute:
            for i in await member.guild.audit_logs(limit=1, oldest_first=False).flatten():
                if i.action.value == 24:
                    if member.guild.get_role(configData["roles"]["equipe_karaoke"]) in member.guild.get_member(
                            i.user.id).roles:
                        e = discord.Embed(
                            title=
                            member.voice.channel.name,
                            description=
                            f"🔈{member.mention} foi calado por {i.user.mention}\n\nUm dia encontrará redenção?",
                            colour=discord.Colour.green()
                        )
                        return await member.guild.get_channel(configData["channels"]["reinoEligos"]).send(
                            embed=e
                        )

        if oldstate.mute:
            for i in await member.guild.audit_logs(limit=1, oldest_first=False).flatten():
                if i.action.value == 24:
                    if member.guild.get_role(configData["roles"]["equipe_karaoke"]) in member.guild.get_member(
                            i.user.id).roles:
                        e = discord.Embed(
                            title=
                            member.voice.channel.name,
                            description=
                            f"🔈{i.user.mention} levou a redenção a {member.mention} e permitiu que voltasse a falar.",
                            colour=discord.Colour.red()
                        )
                        return await member.guild.get_channel(configData["channels"]["reinoEligos"]).send(
                            embed=e
                        )


def setup(bot: commands.Bot):
    bot.add_cog(muteEvents(bot))
