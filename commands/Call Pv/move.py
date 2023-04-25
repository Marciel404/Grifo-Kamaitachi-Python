import discord

from discord.ext import commands
from discord import slash_command
from checks.cargos import has_roles
from classes.buttons import buttonMoveCall
from utils.loader import configData


class move(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @slash_command(name='move', description='Move um membro para a sua call privada')
    @discord.option(name='membro', description='Escolha o membro para puxar para sua call privada')
    @has_roles(
        configData['roles']['ntb'],
        configData['roles']['nvl100'],
        configData['roles']["staff"]['staff1'],
        configData['roles']["staff"]['staff2'],
        configData['roles']['valak']
    )
    async def mv(self, interaction: discord.Interaction, membro: discord.Member):

        call = discord.utils.get(interaction.user.guild.channels, name=f'Pv [{interaction.user.name}]')

        if membro.voice is None:
            return await interaction.response.send_message(f'{membro.mention} não está em um canal de voz',
                                                           ephemeral=True)

        if membro == interaction.user:
            return await interaction.response.send_message(f'Você não pode mover a si mesmo para sua call',
                                                           ephemeral=True)

        if membro.voice.channel == discord.utils.get(interaction.user.guild.channels, name=f'Pv [{membro.name}]'):
            await interaction.response.send_message("Pedido enviado", ephemeral=True)
            try:
                return await membro.send(
                    f'{interaction.user.mention} deseja te mover para a call privada dele, você aceita???',
                    view=buttonMoveCall(call, membro, interaction.user)
                )
            except:
                return await interaction.guild.get_channel(
                    configData["channels"]["commands"]
                ).send(
                    f'{membro.mention}\n{interaction.user} deseja te mover para a call privada dele, você aceita???',
                    view=buttonMoveCall(call, membro, interaction.user))

        if interaction.user.voice.channel != call:
            return await interaction.response.send_message('Você não está no seu canal privado', ephemeral=True)

        if membro.voice.channel != interaction.guild.get_channel(configData['calls']['espera']):
            return await interaction.response.send_message(f'{membro.mention} não está no canal de espera',
                                                           ephemeral=True)

        await membro.move_to(call)

        await interaction.response.send_message(f'{membro.mention} movido para {call}', ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(move(bot))
