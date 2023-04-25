import discord

from discord.ext import commands
from discord import slash_command
from checks.cargos import has_roles
from utils.loader import configData


class disconnect(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(name='disconnect', description='Desconecta um membro da sua call privada')
    @discord.option(name='membro', description='Escolha o membro para desconectar')
    @has_roles(
        configData['roles']['ntb'],
        configData['roles']['nvl100'],
        configData['roles']["staff"]['staff1'],
        configData['roles']["staff"]['staff2'],
        configData['roles']['valak']
    )
    async def dsc(self, interaction, membro: discord.Member = None):

        call = discord.utils.get(interaction.user.guild.channels, name=f'Pv [{interaction.user.name}]')

        if membro.voice is None:
            return await interaction.response.send_message(f'{membro.mention} não está em um canal de voz', ephemeral=True)

        if interaction.user.voice.channel != call:
            return await interaction.response.send_message('Você não está no seu canal privado', ephemeral=True)

        if membro.voice.channel != call:
            return await interaction.response.send_message(f'{membro.mention} não está no seu canal privado', ephemeral=True)

        if membro == interaction.user:
            return await interaction.response.send_message(f'Você não pode desconectar a si mesmo', ephemeral=True)

        await membro.move_to(None)

        await interaction.response.send_message(f'{membro.mention} desconectado com sucesso', ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(disconnect(bot))
