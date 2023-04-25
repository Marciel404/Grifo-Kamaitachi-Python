import asyncio
import discord

from datetime import datetime, timedelta
from discord.ext import commands
from classes.selectmenus import staffSelectAdv, menusCargos, menusCargos2, iniciarCargos, staffSelectNotify
from classes.buttons import confirmButtons
from utils.loader import configData

from db.moderation import adcAdvertencia, RegAtivos, adcNotify

reason = {
    "1": "Flood/spam",
    "2": "Divulgação inadequada",
    "3": "Off topic/mensagem fora de tópico",
    "4": "Menção desnecessária de membros e cargos",
    "5": "Provocação e brigas",
    "6": "Poluição sonora",
    "7": "Atrapalhar o andamento do Karaokê",
    "8": "Denúncias falsas",
    "9": "Linguagem discriminatória",
    "10": "Exposição de membros/ Assédio",
    "11": "Preconceito, discriminação, difamação e/ou desrespeito",
    "12": "Planejar ou exercer raids no servidor",
    "13": "NSFW/ (+18)",
    "14": "Estimular ou praticar atividades ilegais ou que cause banimento de membros",
    "15": "Evasão de punição",
    "16": "Conteúdos graficamente chocantes",
    "17": "Quebra do ToS do Discord",
    "18": "Selfbot",
    "19": "Scam"
}


async def advertenciaButton(selfBot: commands.Bot, interaction: discord.Interaction):
    if interaction.guild.get_role(configData["roles"]["staff"]["staff1"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["staff2"]) in interaction.user.roles\
            or interaction.user.guild_permissions.administrator:

        members = []
        e = discord.Embed(title="advertencia")
        await interaction.response.send_message("São quantas pessoas a advertir?", ephemeral=True)

        def check(m: discord.Message):
            return m.content and m.author == interaction.user

        msg = await selfBot.wait_for("message", check=check, timeout=300)

        await msg.delete()

        for i in range(0, int(msg.content)):
            await interaction.edit_original_response(content=f"Envie o id da pessoa {i + 1}")

            def check(m: discord.Message):
                return m.content and m.author == interaction.user

            msg = await selfBot.wait_for("message", check=check, timeout=300)

            members.append(int(msg.content))

            await msg.delete()

        for i in members:
            if interaction.guild.get_member(i).top_role > interaction.guild.get_member(selfBot.user.id).top_role:
                await interaction.channel.send(
                    content=f"Não consigo punir o membro {interaction.guild.get_member(i).mention}", delete_after=3)
            else:
                e.add_field(
                    name=f"Membro advertido {e.fields.__len__() + 1}",
                    value=interaction.guild.get_member(i).mention
                )

        await interaction.edit_original_response(
            content=f"",
            embed=e,
            view=staffSelectAdv()
        )
    else:
        return await interaction.response.send_message("Sem permissão", ephemeral=True)


async def banButton(selfBot: commands.Bot, interaction: discord.Interaction):
    if interaction.guild.get_role(configData["roles"]["staff"]["staff1"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["staff2"]) in interaction.user.roles \
            or interaction.user.guild_permissions.administrator:

        members = []
        e = discord.Embed(title="Banimento")
        await interaction.response.send_message("São quantas pessoas a Banir?", ephemeral=True)

        def check(m: discord.Message):
            return m.content and m.author == interaction.user

        msg = await selfBot.wait_for("message", check=check, timeout=300)

        await msg.delete()

        for i in range(0, int(msg.content)):
            await interaction.edit_original_response(content=f"Envie o id da pessoa {i + 1}")

            def check(m: discord.Message):
                return m.content and m.author == interaction.user

            msg = await selfBot.wait_for("message", check=check, timeout=300)

            members.append(int(msg.content))

            await msg.delete()

        for i in members:
            if interaction.guild.get_member(i).top_role > interaction.guild.get_member(selfBot.user.id).top_role:
                await interaction.channel.send(
                    content=f"Não consigo punir o membro {interaction.guild.get_member(i).mention}",
                    delete_after=3
                )
            else:
                e.add_field(
                    name=f"Membro a banir {e.fields.__len__() + 1}",
                    value=interaction.guild.get_member(i).mention
                )

        await interaction.edit_original_response(
            content=f"",
            embed=e,
            view=staffSelectAdv()
        )
    else:
        return await interaction.response.send_message("Sem permissão", ephemeral=True)


async def Motivos(selfBot: commands.Bot, interaction: discord.Interaction):
    await interaction.response.edit_message(content="Prontinho", embed=None, view=None)
    e = interaction.message.embeds[0]
    e.description = "**Motivo: {}**".format(reason[interaction.to_dict()["data"]["values"][0]])
    e.set_author(name="Author: {}".format(interaction.user.name), icon_url=interaction.user.display_avatar.url)
    e.set_footer(text=interaction.user.id)
    await interaction.channel.send(embed=e, view=confirmButtons())
    RegAtivos(+1)
    try:
        await interaction.channel.edit(
            name="registros-ativos-{}".format(int(interaction.channel.name.replace("registros-ativos-", "")
                                                  ) - 1
                                              )
        )
    except:
        pass


async def confirm(selfBot: commands.Bot, interaction: discord.Interaction):
    if interaction.guild.get_role(configData["roles"]["staff"]["asmodeus"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["astaroth"]) in interaction.user.roles\
            or interaction.user.guild_permissions.administrator:

        adv1 = interaction.guild.get_role(configData["roles"]["adv1"])
        adv2 = interaction.guild.get_role(configData["roles"]["adv2"])
        adv3 = interaction.guild.get_role(configData["roles"]["adv3"])
        channelLog = interaction.guild.get_channel(configData["channels"]["modlog"])
        embedsFinal = []
        e = interaction.message.embeds[0]
        author = interaction.guild.get_member(int(e.footer.text.strip("<@>")))
        dt = datetime.now().utcnow() - timedelta(hours=3.0)
        RegAtivos(-1)
        await interaction.message.delete()

        match e.title:
            case "Banimento":

                for ef in e.fields:
                    member = interaction.guild.get_member(int(ef.value.strip("<@>")))

                    try:
                        await member.send(content="https://discord.gg/Wm7wxJzJ", embed=discord.Embed(
                            title="Banimento",
                            colour=discord.Colour.red()
                        ) \
                            .add_field(name="Membro Banir", value=member.name, inline=False) \
                            .add_field(name="Banido por", value=author.mention, inline=False) \
                            .add_field(name="Aprovado por", value=interaction.user.mention, inline=False) \
                            .add_field(name="Motivo", value=e.description.replace("Motivo: ", ""), inline=False) \
                            .add_field(name="Data/Hora", value=dt.strftime("%d/%m/%Y as %H:%M"), inline=False) \
                            .set_thumbnail(url=interaction.guild.icon.url) \
                            .set_footer(text=member.id))
                    except:
                        pass

                    await member.ban(delete_message_seconds=86400, reason="Acumulo de advertencia")
                    embedsFinal.append(
                        discord.Embed(
                            title="Banimento",
                            colour=discord.Colour.red()
                        ) \
                            .add_field(name="Membro Banir", value=member.name, inline=False) \
                            .add_field(name="Banido por", value=author.mention, inline=False) \
                            .add_field(name="Aprovado por", value=interaction.user.mention, inline=False) \
                            .add_field(name="Motivo", value=e.description.replace("Motivo: ", ""), inline=False) \
                            .add_field(name="Data/Hora", value=dt.strftime("%d/%m/%Y as %H:%M"), inline=False) \
                            .set_thumbnail(url=interaction.guild.icon.url) \
                            .set_footer(text=member.id)
                    )
                await channelLog.send(embeds=embedsFinal)

            case "advertencia":

                for ef in e.fields:
                    member = interaction.guild.get_member(int(ef.value.strip("<@>")))
                    try:
                        if adv3 in member.roles:

                            try:
                                await member.send(content="https://discord.gg/Wm7wxJzJ", embed=discord.Embed(
                                    title="Ban",
                                    colour=discord.Colour.red()
                                ) \
                                    .add_field(name="Membro advertido", value=member.name, inline=False) \
                                    .add_field(name="Banido por", value=author.mention, inline=False) \
                                    .add_field(name="Aprovado por", value=interaction.user.mention, inline=False) \
                                    .add_field(name="Motivo", value="Acumulo de advertencia", inline=False) \
                                    .add_field(name="Data/Hora", value=dt.strftime("%d/%m/%Y as %H:%M"), inline=False) \
                                    .set_thumbnail(url=interaction.guild.icon.url) \
                                    .set_footer(text=member.id))
                            except:
                                pass

                            await member.ban(delete_message_seconds=86400, reason=e.description.replace("Motivo: ", ""))
                            embedsFinal.append(
                                discord.Embed(
                                    title="Ban",
                                    colour=discord.Colour.red()
                                ) \
                                    .add_field(name="Membro advertido", value=member.name, inline=False) \
                                    .add_field(name="Banido por", value=author.mention, inline=False) \
                                    .add_field(name="Aprovado por", value=interaction.user.mention, inline=False) \
                                    .add_field(name="Motivo", value="Acumulo de advertencia", inline=False) \
                                    .add_field(name="Data/Hora", value=dt.strftime("%d/%m/%Y as %H:%M"), inline=False) \
                                    .set_thumbnail(url=interaction.guild.icon.url) \
                                    .set_footer(text=member.id)
                            )

                        if adv2 in member.roles and adv3 not in member.roles:
                            await member.add_roles(adv3)
                            await member.timeout(datetime.now().utcnow() + timedelta(days=2), reason="advertencia 1")
                            embedsFinal.append(
                                discord.Embed(
                                    title="Advertencia",
                                    colour=discord.Colour.yellow()
                                ) \
                                    .add_field(name="Membro advertido", value=member.mention, inline=False) \
                                    .add_field(name="Advertido por", value=author.mention, inline=False) \
                                    .add_field(name="Aprovado por", value=interaction.user.mention, inline=False) \
                                    .add_field(name="Motivo", value=e.description.replace("Motivo: ", ""), inline=False) \
                                    .add_field(name="Data/Hora", value=dt.strftime("%d/%m/%Y as %H:%M"), inline=False) \
                                    .set_thumbnail(url=interaction.guild.icon.url) \
                                    .set_footer(text=member.id)

                            )
                            adcAdvertencia(
                                author,
                                member,
                                interaction.user,
                                e.description.replace("Motivo: ", ""),
                                dt.strftime("%d/%m/%Y as %H:%M"),
                                + 1
                            )
                        if adv1 in member.roles and adv2 not in member.roles:
                            await member.add_roles(adv2)
                            await member.timeout(datetime.now().utcnow() + timedelta(hours=12), reason="advertencia 1")
                            embedsFinal.append(
                                discord.Embed(
                                    title="Advertencia",
                                    colour=discord.Colour.yellow()
                                ) \
                                    .add_field(name="Membro advertido", value=member.mention, inline=False) \
                                    .add_field(name="Advertido por", value=author.mention, inline=False) \
                                    .add_field(name="Aprovado por", value=interaction.user.mention, inline=False) \
                                    .add_field(name="Motivo", value=e.description.replace("Motivo: ", ""), inline=False) \
                                    .add_field(name="Data/Hora", value=dt.strftime("%d/%m/%Y as %H:%M"), inline=False) \
                                    .set_thumbnail(url=interaction.guild.icon.url) \
                                    .set_footer(text=member.id)
                            )
                            adcAdvertencia(
                                author,
                                member,
                                interaction.user,
                                e.description.replace("Motivo: ", ""),
                                dt.strftime("%d/%m/%Y as %H:%M"),
                                + 1
                            )
                        if adv1 not in member.roles:
                            await member.add_roles(adv1)
                            await member.timeout(datetime.now().utcnow() + timedelta(hours=2), reason="advertencia 1")
                            embedsFinal.append(
                                discord.Embed(
                                    title="Advertencia",
                                    colour=discord.Colour.yellow()
                                ) \
                                    .add_field(name="Membro advertido", value=member.mention, inline=False) \
                                    .add_field(name="Advertido por", value=author.mention, inline=False) \
                                    .add_field(name="Aprovado por", value=interaction.user.mention, inline=False) \
                                    .add_field(name="Motivo", value=e.description.replace("Motivo: ", ""), inline=False) \
                                    .add_field(name="Data/Hora", value=dt.strftime("%d/%m/%Y as %H:%M"), inline=False) \
                                    .set_thumbnail(url=interaction.guild.icon.url) \
                                    .set_footer(text=member.id)
                            )
                            adcAdvertencia(
                                author,
                                member,
                                interaction.user,
                                e.description.replace("Motivo: ", ""),
                                dt.strftime("%d/%m/%Y as %H:%M"),
                                + 1
                            )
                        await asyncio.sleep(2)
                    except Exception as error:
                        pass
                await channelLog.send(embeds=embedsFinal)

            case "Adicionar cargo":
                for ef in e.fields:
                    try:
                        member = interaction.guild.get_member(int(ef.value.strip("<@>")))
                        await member.add_roles(
                            interaction.guild.get_role(
                                int(e.description.replace("Cargo a adicionar: ", "").strip("<@&>"))
                            )
                        )
                    except:
                        pass
            case "Remover cargo":
                for ef in e.fields:
                    member = interaction.guild.get_member(int(ef.value.strip("<@>")))
                    cargo = interaction.guild.get_role(
                        int(e.description.replace("Cargo a remover: ", "").strip("<@&>"))
                    )
                    try:
                        await member.remove_roles(cargo)
                    except:
                        await interaction.channel.send(f"O membro {member.mention} não tem o cargo {cargo}",
                                                       delete_after=5)
        try:
            await interaction.channel.edit(
                name="registros-ativos-{}".format(int(interaction.channel.name.replace("registros-ativos-", "")
                                                      ) - 1
                                                  )
            )
        except:
            pass

    else:
        return await interaction.response.send_message("Sem permissão", ephemeral=True)


async def deny(selfBot: commands.Bot, interaction: discord.Interaction):
    if interaction.guild.get_role(configData["roles"]["staff"]["asmodeus"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["astaroth"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["staff1"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["staff2"]) in interaction.user.roles\
            or interaction.user.guild_permissions.administrator:
        await interaction.message.delete()
        RegAtivos(-1)
    else:
        return await interaction.response.send_message("Sem permissão", ephemeral=True)


async def cargosButton(selfBot: commands.Bot, interaction: discord.Interaction):
    if interaction.guild.get_role(configData["roles"]["staff"]["asmodeus"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["astaroth"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["capitaes_karaoke"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["capitaes_poem"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["capitaes_arte"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["capitaes_evento"]) in interaction.user.roles\
            or interaction.user.guild_permissions.administrator:

        await interaction.response.send_message(view=iniciarCargos(), ephemeral=True)
    else:
        await interaction.response.send_message("Sem permissão", ephemeral=True)


async def selectIniciar(selfBot: commands.Bot, interaction: discord.Interaction):
    value = interaction.to_dict()["data"]["values"][0]

    if value == "adc":
        await cargosAdicionar(selfBot, interaction)
    if value == "rmv":
        await cargosRemover(selfBot, interaction)


async def cargosAdicionar(selfBot: commands.Bot, interaction: discord.Interaction):
    members = []
    e = discord.Embed(title="Adicionar cargo")
    await interaction.response.edit_message(content="São quantas pessoas a adicionar?", view=None)

    def check(m: discord.Message):
        return m.content and m.author == interaction.user

    msg = await selfBot.wait_for("message", check=check, timeout=300)

    await msg.delete()

    for i in range(0, int(msg.content)):
        await interaction.edit_original_response(content=f"Envie o id da pessoa {i + 1}")

        def check(m: discord.Message):
            return m.content and m.author == interaction.user

        msg = await selfBot.wait_for("message", check=check, timeout=300)

        members.append(int(msg.content))

        await msg.delete()

    for i in members:
        if interaction.guild.get_member(i).top_role > interaction.guild.get_member(selfBot.user.id).top_role:
            await interaction.channel.send(
                content=f"Não consigo adicionar o cargo a {interaction.guild.get_member(i).mention}",
                delete_after=3
            )
        else:
            e.add_field(
                name=f"Membro a adicionar {e.fields.__len__() + 1}",
                value=interaction.guild.get_member(i).mention
            )

    await interaction.edit_original_response(
        content=f"",
        embed=e,
        view=menusCargos()
    )


async def cargosRemover(selfBot: commands.Bot, interaction: discord.Interaction):
    members = []
    e = discord.Embed(title="Remover cargo")
    await interaction.response.edit_message(content="São quantas pessoas a remover?", view=None)

    def check(m: discord.Message):
        return m.content and m.author == interaction.user

    msg = await selfBot.wait_for("message", check=check, timeout=300)

    await msg.delete()

    for i in range(0, int(msg.content)):
        await interaction.edit_original_response(content=f"Envie o id da pessoa {i + 1}")

        def check(m: discord.Message):
            return m.content and m.author == interaction.user

        msg = await selfBot.wait_for("message", check=check, timeout=300)

        members.append(int(msg.content))

        await msg.delete()

    for i in members:
        if interaction.guild.get_member(i).top_role > interaction.guild.get_member(selfBot.user.id).top_role:
            await interaction.channel.send(
                content=f"Não consigo remover o cargo de {interaction.guild.get_member(i).mention}",
                delete_after=3
            )
        else:
            e.add_field(
                name=f"Membro a remover {e.fields.__len__() + 1}",
                value=interaction.guild.get_member(i).mention
            )

    await interaction.edit_original_response(
        content=f"",
        embed=e,
        view=menusCargos()
    )


async def selectCargos(selfBot: commands.Bot, interaction: discord.Interaction):
    value = interaction.to_dict()["data"]["values"][0]
    asmodeus = interaction.guild.get_role(configData["roles"]["staff"]["asmodeus"])
    astaroth = interaction.guild.get_role(configData["roles"]["staff"]["astaroth"])

    capKaraoke = interaction.guild.get_role(configData["roles"]["capitaes_karaoke"])
    capPoem = interaction.guild.get_role(configData["roles"]["capitaes_poem"])
    capArte = interaction.guild.get_role(configData["roles"]["capitaes_arte"])
    capEvento = interaction.guild.get_role(configData["roles"]["capitaes_evento"])

    if value == "eligos" and capKaraoke in interaction.user.roles \
            or value == "eligos" and asmodeus in interaction.user.roles \
            or value == "eligos" and astaroth in interaction.user.roles:
        await interaction.response.edit_message(
            view=menusCargos2("eligos")
        )

    elif value == "vagantes" and capPoem in interaction.user.roles \
            or value == "vagantes" and asmodeus in interaction.user.roles \
            or value == "vagantees" and astaroth in interaction.user.roles:
        await interaction.response.edit_message(
            view=menusCargos2("vagantes")
        )

    elif value == "naberios" and capArte in interaction.user.roles \
            or value == "naberios" and asmodeus in interaction.user.roles \
            or value == "naberios" and astaroth in interaction.user.roles:
        await interaction.response.edit_message(
            view=menusCargos2("naberios")
        )

    elif value == "gremorys" and capEvento in interaction.user.roles \
            or value == "gremorys" and asmodeus in interaction.user.roles \
            or value == "gremorys" and astaroth in interaction.user.roles:
        await interaction.response.edit_message(
            view=menusCargos2("gremorys")
        )

    else:
        await interaction.response.send_message("Sem permissão", ephemeral=True)


async def selectCargos2(selfBot: commands.Bot, interaction: discord.Interaction):
    valueI = interaction.to_dict()["data"]["values"][0]
    await interaction.response.edit_message(content="Prontinho", embed=None, view=None)
    e = interaction.message.embeds[0]
    dc = ""

    if "cap" in valueI:
        cargo = interaction.guild.get_role(configData["roles"][f"capitaes_{str(valueI).replace('cap ', '')}"]).mention
        if e.title == "Adicionar cargo":
            dc = f"Cargo a adicionar: {cargo}"
        if e.title == "Remover cargo":
            dc = f"Cargo a remover: {cargo}"
        e.set_author(name="Author: {}".format(interaction.user.name), icon_url=interaction.user.display_avatar.url)
        e.description = dc

        e.set_footer(text=interaction.user.id)
        await interaction.channel.send(embed=e, view=confirmButtons())
        try:
            await interaction.channel.edit(
                name="registros-ativos-{}".format(int(interaction.channel.name.strip("registros-ativos-")
                                                      ) + 1
                                                  )
            )
        except:
            pass
    else:
        cargo = interaction.guild.get_role(configData['roles'][f'equipe_{valueI}']).mention
        if e.title == "Adicionar cargo":
            dc = f"Cargo a adicionar: {cargo}"
        if e.title == "Remover cargo":
            dc = f"Cargo a remover: {cargo}"
        e.set_author(name="Author: {}".format(interaction.user.name), icon_url=interaction.user.display_avatar.url)
        e.description = dc

        e.set_footer(text=interaction.user.id)
        await interaction.channel.send(embed=e, view=confirmButtons())
        RegAtivos(+1)
        try:
            await interaction.channel.edit(
                name="registros-ativos-{}".format(int(interaction.channel.name.strip("registros-ativos-")
                                                      ) + 1
                                                  )
            )
        except:
            pass


async def avisoButton(selfBot: commands.Bot, interaction: discord.Interaction):
    if interaction.guild.get_role(configData["roles"]["staff"]["asmodeus"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["astaroth"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["staff1"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["staff2"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["acacus"]) in interaction.user.roles \
            or interaction.guild.get_role(configData["roles"]["staff"]["ormenus"]) in interaction.user.roles \
            or interaction.user.guild_permissions.administrator:
        members = []
        e = discord.Embed(title="Notificação")
        await interaction.response.send_message("São quantas pessoas a notificar?", ephemeral=True)

        def check(m: discord.Message):
            return m.content and m.author == interaction.user

        msg = await selfBot.wait_for("message", check=check, timeout=300)

        await msg.delete()

        for i in range(0, int(msg.content)):
            await interaction.edit_original_response(content=f"Envie o id da pessoa {i + 1}")

            def check(m: discord.Message):
                return m.content and m.author == interaction.user

            msg = await selfBot.wait_for("message", check=check, timeout=300)

            members.append(int(msg.content))

            await msg.delete()

        for i in members:
            e.add_field(
                name=f"Membro a avisar {e.fields.__len__() + 1}",
                value=interaction.guild.get_member(i).mention
            )

        await interaction.edit_original_response(
            content=f"",
            embed=e,
            view=staffSelectNotify()
        )
    else:
        await interaction.response.send_message("Sem permissão", ephemeral=True)


async def MotivosNotify(selfBot: commands.Bot, interaction: discord.Interaction):
    channelLog = interaction.guild.get_channel(configData["channels"]["modlog"])
    e = interaction.message.embeds[0]

    await interaction.response.edit_message(content="Notificação concluida", embed=None, view=None)

    dt = datetime.utcnow() - timedelta(hours=3.0)
    e2 = discord.Embed(title="Notificação",
                       colour=discord.Colour.green())
    e2.description = f"""
Olá tudo bem? Você recebeu uma notificação pelo
motivo: {reason[interaction.to_dict()["data"]["values"][0]]}

Lembre-se, Notificação não possui peso, você
não sofreu advertência ou algo que gere seu
banimento. As notificações existem apenas para
te deixar mais por dentro do assunto.
Ou seja, relaxe
    """
    for ef in e.fields:
        member = interaction.guild.get_member(int(ef.value.strip("<@>")))

        adcNotify(
            interaction.user,
            member,
            reason[interaction.to_dict()["data"]["values"][0]],
            dt.strftime("%d/%m/%Y as %H:%M"),
            + 1
        )

        try:

            await member.send(embed=e2)

            er = discord.Embed(title="Notificação", colour=discord.Colour.green()) \
                .add_field(name="Notificado", value=member.mention, inline=False) \
                .add_field(name="Autor", value=interaction.user.mention, inline=False) \
                .add_field(name="Motivo", value = reason[interaction.to_dict()["data"]["values"][0]]) \
                .set_footer(text=member.id) \
                .set_thumbnail(url=interaction.guild.icon.url)

            await channelLog.send(embed=er)

        except:

            er = discord.Embed(title="Notificação") \
                .add_field(name="Notificado", value=member.mention, inline=False) \
                .add_field(name="Autor", value=interaction.user.mention, inline=False) \
                .set_footer(text=member.id) \
                .add_field(name="Motivo", value=reason[interaction.to_dict()["data"]["values"][0]]) \
                .set_thumbnail(url=interaction.guild.icon.url)

            await channelLog.send(content=member.mention, embed=er)
