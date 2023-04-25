import discord

from discord.ui import Button

from utils.loader import configData


class buttonMoveCall(discord.ui.View):

    def __init__(self, call: discord.VoiceChannel, membro: discord.Member, author: discord.Member):
        self.call = call
        self.membro = membro
        self.author = author

        super().__init__(timeout=500)

    @discord.ui.button(label='Aceitar', style=discord.ButtonStyle.blurple)
    async def aceitar(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.membro.id:
            return await interaction.response.send_message("Esse botão não te pertence", ephemeral=True)
        await self.membro.move_to(self.call)
        await interaction.message.delete()
        await interaction.response.send_message("Prontinho", ephemeral=True)

    @discord.ui.button(label='Recusar', style=discord.ButtonStyle.blurple)
    async def recusar(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.membro.id:
            return await interaction.response.send_message("Esse botão não te pertence", ephemeral=True)
        try:
            await self.author.send(f"O membro {self.membro} rejeitou seu pedido para ser movido para sua call")
        except:
            await interaction.guild.get_channel(
                configData["channels"]["commands"]).send(
                f"{self.author.mention}\nO membro {self.membro} rejeitou seu pedido para ser movido para sua call"
            )
        await interaction.message.delete()


class butonsListParticipar(discord.ui.View):

    def __init__(self, **kwargs):
        super().__init__()

        self.add_item(Button(
            label="Entrar",
            style=discord.ButtonStyle.green,
            custom_id="entrarEvento"
        )
        )

        self.add_item(Button(
            label="Sair",
            style=discord.ButtonStyle.red,
            custom_id="sairEvento"
        )
        )

        self.add_item(Button(
            label="Finalizar lista",
            style=discord.ButtonStyle.gray,
            custom_id="finalizarLista"
        )
        )


class Ticket(discord.ui.View):

    def __init__(self, **kwargs):
        super().__init__()

        for i in range(0, int(kwargs.get("qnt"))):
            self.add_item(
                Button(
                    style=discord.ButtonStyle.blurple,
                    label=f"{kwargs.get('name_list')[i]}",
                    custom_id=f"abrirTicket-{kwargs.get('idcategorias')[i]}"
                )
            )


class AdonTicket(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='🔒 Fechar ticket',
                style=discord.ButtonStyle.blurple,
                custom_id="closeTicket"
            )
        )


class claimButton(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='🔒 Fechar ticket',
                style=discord.ButtonStyle.blurple,
                custom_id="closeTicket"
            )
        )

        self.add_item(
            Button(
                label='Claim',
                style=discord.ButtonStyle.blurple,
                custom_id="claim"
            )
        )


class AdonTicket2(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label='🔓 Abrir ticket',
                style=discord.ButtonStyle.blurple,
                custom_id="openTicket"
            )
        )
        self.add_item(
            Button(
                label='🛑 Deletar Ticket',
                style=discord.ButtonStyle.blurple,
                custom_id="deleteTicket"
            )
        )


class jumpto(discord.ui.View):

    def __init__(self, url):
        super().__init__()

        self.add_item(
            Button(
                label='Atalho para o ticket',
                style=discord.ButtonStyle.url,
                url=url
            )
        )


class buttonsStaff(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label="BAN",
                custom_id="banButton",
                style=discord.ButtonStyle.danger
            )
        )
        self.add_item(
            Button(
                label="ADVERTENCIA",
                custom_id="advertenciaButton",
                style=discord.ButtonStyle.blurple
            )
        ),
        self.add_item(
            Button(
                label="Notificar",
                custom_id="avisoButton",
                style=discord.ButtonStyle.secondary
            )
        )
        self.add_item(
            Button(
                label="CARGOS",
                custom_id="cargosButton",
                style=discord.ButtonStyle.green
            )
        )


class confirmButtons(discord.ui.View):

    def __init__(self):
        super().__init__()

        self.add_item(
            Button(
                label="✅",
                custom_id="confirm",
                style=discord.ButtonStyle.danger
            )
        )
        self.add_item(
            Button(
                label="❌",
                custom_id="deny",
                style=discord.ButtonStyle.danger
            )
        )
