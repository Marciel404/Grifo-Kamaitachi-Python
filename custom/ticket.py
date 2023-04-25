import discord
import os
import NewFunctionsPYC

from datetime import datetime, timedelta
from discord.ext import commands
from classes.buttons import AdonTicket, AdonTicket2, jumpto, claimButton
from classes.selectmenus import createSelect
from utils.loader import configData
from funcs.ticket import verify_pastas


async def ticket_select(selfbot: commands.Bot, interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    name_list = []
    idcategorias = []
    for i in interaction.to_dict()["message"]["components"][0]["components"][0]["options"]:
        name_list.append(i["label"])
        idcategorias.append(i["value"])

    await interaction.followup.edit_message(
        interaction.message.id,
        view=createSelect(
            qnt=interaction.to_dict()["message"]["components"][0]["components"][0]["options"].__len__(),
            name_list=name_list,
            idcategorias=idcategorias
        )
    )

    await interaction.followup.send('Criando ticket', ephemeral=True)

    await verify_pastas()

    ticket = f'ticket-{interaction.user.id}'

    dt = datetime.now().utcnow() - timedelta(hours=3.0)

    c = interaction.to_dict()["data"]["values"][0]

    categoria: discord.CategoryChannel = discord.utils.get(interaction.guild.categories, id=int(c[3:]))

    for i in categoria.text_channels:

        if ticket in i.name:
            return await interaction.followup.send('Ticket já existente, encerre o ultimo para criar outro',
                                                   ephemeral=True)

    guild = interaction.guild

    member = interaction.user

    astaroth: discord.Role = discord.utils.get(guild.roles, id=configData["roles"]["staff"]["astaroth"])
    ormenus: discord.Role = discord.utils.get(guild.roles, id=configData["roles"]["staff"]["ormenus"])
    acacus: discord.Role = discord.utils.get(guild.roles, id=configData["roles"]["staff"]["acacus"])

    overwrites = {

        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True,attach_files=True),
        acacus: discord.PermissionOverwrite(read_messages=True,attach_files=True)

    }

    for file in os.listdir(f"./tickets/{categoria.name.removeprefix('ticket ')}"):
        if file.endswith(".txt"):
            try:
                if file.startswith(f'{interaction.user.id}'):
                    os.remove(
                        f"./tickets/{categoria.name.removeprefix('ticket ')}/{interaction.user.id}.txt")
            except:
                pass

    with open(f'./tickets/{categoria.name.removeprefix("ticket ")}/{interaction.user.id}.txt', 'a') as f:
        f.write(
            f'Data: {dt.strftime("%d/%m/%Y as %H:%M")} \nTicket de: {interaction.user.id} \nNome no momento: {interaction.user.name}\n')

    channel = await interaction.guild.create_text_channel(
        name=ticket,
        overwrites=overwrites,
        category=categoria
    )

    if interaction.message.author.discriminator == "0000":
        if interaction.message.author.avatar != None:
            web = await channel.create_webhook(
                name=interaction.message.author.name,
                avatar=await interaction.message.author.avatar.read()
            )
        else:
            web = await channel.create_webhook(name=interaction.message.author.name)

    await interaction.followup.send(
        'Ticket criado com sucesso',
        view=jumpto(f'https://discordapp.com/channels/{interaction.guild.id}/{channel.id}'),
        ephemeral=True
    )

    if "(Atendido)" not in member.display_name:
        try:
            await member.edit(nick=f"{member.display_name}(Atendido)")
        except:
            pass
    e = discord.Embed(
        title=f'Ticket de {interaction.user}',
        description=dt.strftime("Aberto as %H:%M de %d/%m/%Y")
    )
    e.set_footer(text=interaction.user.id)

    mention = ""
    if categoria.id == configData["categories"]["ticket_chats"]:
        mention = ormenus.mention
    elif categoria.id == configData["categories"]["ticket_calls"]:
        mention = acacus.mention
    elif categoria.id == configData["categories"]["ticket_privado"]:
        mention = astaroth.mention
    elif categoria.id == configData["categories"]["ticket_outros"]:
        mention = acacus.mention

    try:
        await web.send(content=f'{interaction.user.mention} {mention}', embed=e, view=claimButton())
    except:
        await channel.send(content=f'{interaction.user.mention} {mention}', embed=e, view=claimButton())

    e = NewFunctionsPYC.EmbedBuilder()

    if categoria.id == configData["categories"]["ticket_chats"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Criado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Chats")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0x2ECC71)

        await interaction.guild.get_channel(configData["logs"]["log_create_chats"]).send(embed=e.build())

    elif categoria.id == configData["categories"]["ticket_calls"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Criado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Calls")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0x2ECC71)

        await interaction.guild.get_channel(configData["logs"]["log_create_calls"]).send(embed=e.build())

    elif categoria.id == configData["categories"]["ticket_privado"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Criado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Privado")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0x2ECC71)

        await interaction.guild.get_channel(configData["logs"]["log_create_privado"]).send(embed=e.build())

    elif categoria.id == configData["categories"]["ticket_outros"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Criado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Outros")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0x2ECC71)

        await interaction.guild.get_channel(configData["logs"]["log_create_outros"]).send(embed=e.build())


async def closeTicket(selfbot: commands.Bot, interaction: discord.Interaction):
    member = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))

    acacus = discord.utils.get(interaction.guild.roles, id=configData["roles"]["staff"]["acacus"])

    overwrites = {

        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),

        member: discord.PermissionOverwrite(read_messages=False),

        acacus: discord.PermissionOverwrite(read_messages=True)

    }

    e = discord.Embed(
        description=f'🔒Ticket de {member} fechado por {interaction.user.mention} \nClique no 🔓 para abrir')
    e.set_footer(text=member.id)

    await interaction.channel.edit(overwrites=overwrites)

    await interaction.message.delete()

    try:
        p = await interaction.channel.webhooks()
        web = await selfbot.fetch_webhook(p[0].id)
        await web.send(embed=e, view=AdonTicket2())
    except:
        await interaction.channel.send(embed=e, view=AdonTicket2())

    await interaction.user.edit(nick=f"{interaction.user.display_name.removesuffix('(atentende)')}")

    await member.edit(nick=f"{member.display_name.removesuffix('(Atendido)')}")

    e = NewFunctionsPYC.EmbedBuilder()

    if interaction.channel.category.id == configData["categories"]["ticket_chats"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Fechado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Chats")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xFEE75C)

        await interaction.guild.get_channel(configData["logs"]["log_create_chats"]).send(embed=e.build())

    elif interaction.channel.category.id == configData["categories"]["ticket_calls"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Fechado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Calls")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xFEE75C)

        await interaction.guild.get_channel(configData["logs"]["log_create_calls"]).send(embed=e.build())

    elif interaction.channel.category.id == configData["categories"]["ticket_privado"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Fechado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Privado")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xFEE75C)

        await interaction.guild.get_channel(configData["logs"]["log_create_privado"]).send(embed=e.build())

    elif interaction.channel.category.id == configData["categories"]["ticket_outros"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Fechado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Outros")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xFEE75C)

        await interaction.guild.get_channel(configData["logs"]["log_create_outros"]).send(embed=e.build())


async def openTicket(selfbot: commands.Bot, interaction: discord.Interaction):
    member = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))

    acacus = discord.utils.get(interaction.guild.roles, id=configData["roles"]["staff"]["acacus"])

    overwrites = {

        member: discord.PermissionOverwrite(read_messages=True, attach_files=True),
        acacus: discord.PermissionOverwrite(read_messages=True, attach_files=True),
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),

    }

    await interaction.channel.edit(overwrites=overwrites)

    await interaction.message.delete()

    e = discord.Embed(title=f'Ticket de {member} aberto 🔓')
    e.set_footer(text=member.id)

    try:
        p = await interaction.channel.webhooks()
        web = await selfbot.fetch_webhook(p[0].id)
        await web.send(embed=e, view=claim())
    except:
        await interaction.channel.send(embed=e, view=claimButton())

    e = NewFunctionsPYC.EmbedBuilder()

    if interaction.channel.category.id == configData["categories"]["ticket_chats"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Aberto", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Chats")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xE67E22)

        await interaction.guild.get_channel(configData["logs"]["log_create_chats"]).send(embed=e.build())

    elif interaction.channel.category.id == configData["categories"]["ticket_calls"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Aberto", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Calls")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xE67E22)

        await interaction.guild.get_channel(configData["logs"]["log_create_calls"]).send(embed=e.build())

    elif interaction.channel.category.id == configData["categories"]["ticket_privado"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Aberto", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Privado")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xE67E22)

        await interaction.guild.get_channel(configData["logs"]["log_create_privado"]).send(embed=e.build())

    elif interaction.channel.category.id == configData["categories"]["ticket_outros"]:

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Aberto", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Outros")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xE67E22)

        await interaction.guild.get_channel(configData["logs"]["log_create_outros"]).send(embed=e.build())


async def deleteTicket(selfbot: commands.Bot, interaction: discord.Interaction):
    member = interaction.guild.get_member(
        int(interaction.message.embeds[0].footer.text)
    )

    try:
        await member.edit(nick=f"{member.display_name.removesuffix('(Atendido)')}")
    except:
        pass

    try:
        await interaction.user.edit(nick=f"{interaction.user.display_name.removesuffix('(Atendente)')}")
    except:
        pass

    e = NewFunctionsPYC.EmbedBuilder()

    if interaction.channel.category.id == configData["categories"]["ticket_chats"]:
        await interaction.guild.get_channel(configData["logs"]["log_transcript_chats"]).send(
            content=f"Ticket de {member.name}", file=discord.File(
                './tickets/{}/{}.txt'.format(interaction.channel.category.name.removeprefix("ticket "), member.id),
                f'Ticket de {member.name}.txt'))

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Deletado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Chats")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xE74C3C)

        await interaction.guild.get_channel(configData["logs"]["log_create_chats"]).send(embed=e.build())

    elif interaction.channel.category.id == configData["categories"]["ticket_calls"]:
        await interaction.guild.get_channel(configData["logs"]["log_transcript_calls"]).send(
            content=f"Ticket de {member.name}", file=discord.File(
                './tickets/{}/{}.txt'.format(interaction.channel.category.name.removeprefix("ticket "), member.id),
                f'Ticket de {member.name}.txt'))

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Deletado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Calls")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xE74C3C)

        await interaction.guild.get_channel(configData["logs"]["log_create_calls"]).send(embed=e.build())

    elif interaction.channel.category.id == configData["categories"]["ticket_privado"]:
        await interaction.guild.get_channel(configData["logs"]["log_transcript_privado"]).send(
            content=f"Ticket de {member.name}", file=discord.File(
                './tickets/{}/{}.txt'.format(interaction.channel.category.name.removeprefix("ticket "), member.id),
                f'Ticket de {member.name}.txt'))

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Deletado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Privado")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xE74C3C)

        await interaction.guild.get_channel(configData["logs"]["log_create_privado"]).send(embed=e.build())

    elif interaction.channel.category.id == configData["categories"]["ticket_outros"]:
        await interaction.guild.get_channel(configData["logs"]["log_transcript_outros"]).send(
            content=f"Ticket de {member.name}", file=discord.File(
                './tickets/{}/{}.txt'.format(interaction.channel.category.name.removeprefix("ticket "), member.id),
                f'Ticket de {member.name}.txt'))

        e.add_field(name="INFO", value=f"Ticket de: {member.mention}\nAção: Deletado", inline=False)
        e.add_field(name="Tipo", value=f"Problemas em Outros")
        e.set_footer(text=f"author: {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        e.set_color(0xE74C3C)

        await interaction.guild.get_channel(configData["logs"]["log_create_outros"]).send(embed=e.build())

    await interaction.channel.delete()


async def claim(selfbot: commands.Bot, interaction: discord.Interaction):
    try:

        dt = datetime.now().utcnow() - timedelta(hours=3.0)
        guild = interaction.guild
        member = interaction.guild.get_member(int(interaction.message.embeds[0].footer.text))
        acacus = discord.utils.get(guild.roles, id=configData["roles"]["staff"]["acacus"])
        claimer = interaction.user

        if interaction.user == member:
            return await interaction.response.send_message("Sem permissão para isso", ephemeral=True)

        overwrites = {

            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            claimer: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            acacus: discord.PermissionOverwrite(read_messages=True, send_messages=False)

        }

        linha_especifica = 3
        texto = f"\nData claimed: {dt.strftime('%d/%m/%Y as %H:%M')}\natendente: {interaction.user.id}\nNome no momento: {interaction.user.name}\n"
        file = open(f'tickets/{interaction.channel.category.name.removeprefix("ticket ")}/{member.id}.txt', 'r')
        lines = file.readlines()
        file.close()
        lines.insert(linha_especifica, texto)
        file = open(f'tickets/{interaction.channel.category.name.removeprefix("ticket ")}/{member.id}.txt', 'w')
        file.writelines(lines)
        file.close()

        if "(Atendente)" not in claimer.display_name:
            try:
                await claimer.edit(nick=f"{claimer.display_name}(Atendente)")
            except:
                pass

        await interaction.response.edit_message(view=AdonTicket())

        await interaction.channel.edit(overwrites=overwrites)

    except Exception as error:
        print(error)
