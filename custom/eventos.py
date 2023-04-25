import os
import discord
from discord.ext import commands
from utils.loader import configData


async def entrarEvento(selfbot: commands.Bot, interaction: discord.Interaction):
    try:
        ee = interaction.message.embeds[0].description
        if str(interaction.user.id) in ee:
            return await interaction.response.send_message("Você já está na lista", ephemeral=True)
    except:
        pass

    with open("listaEvento.txt", "a", encoding="UTF-8") as lista:
        lista.write(f"\n{interaction.user.mention}")

    participantes = open("listaEvento.txt", "r")
    lines = participantes.read()
    participantes.close()

    e = discord.Embed(title="Lista de participantes", description=lines)

    await interaction.message.edit(embed=e)

    await interaction.response.send_message("Adicionado a lista", ephemeral=True)


async def sairEvento(selfbot: commands.Bot, interaction: discord.Interaction):
    try:
        ee = interaction.message.embeds[0].description
        if str(interaction.user.id) not in ee:
            return await interaction.response.send_message("Você não está na lista", ephemeral=True)
    except:
        pass

    ee = interaction.message.embeds[0].description

    os.remove("listaEvento.txt")

    with open("listaEvento.txt", "a") as participantes:

        participantes.write(ee.replace(f"{interaction.user.mention}", ""))

    participantes = open("listaEvento.txt", "r")
    lines = participantes.read()
    participantes.close()

    e = discord.Embed(title="Lista de participantes", description=lines)

    await interaction.message.edit(embed=e)

    await interaction.response.send_message("removido da lista", ephemeral=True)


async def finalizarLista(selfbot: commands.Bot, interaction: discord.Interaction):
    if interaction.guild.get_role(configData["roles"]["staff"]["staff1"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["staff2"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["capitaes_evento"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["capitaes_karaoke"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["capitaes_arte"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["capitaes_poem"]) in interaction.user.roles:

        await interaction.response.edit_message(view=None)

    else:

        await interaction.response.send_message("você não tem permissão para isso", ephemeral=True)
