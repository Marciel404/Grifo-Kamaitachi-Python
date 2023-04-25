import discord
import custom
import NewFunctionsPYC

from discord.ext import commands
from db.moderation import verifyAdvertencia
from funcs.tasks import Tasks


class generals(commands.Cog):

    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):

        await verifyAdvertencia(member)

        if member.guild.id == 865014447113502740:
            e = discord.Embed(title="Revogação de bans",
                              description=
                              '''
O unico motivo para unban é a contestação da aplicação de uma punição. O ban só pode ser removido caso a punição tenha sido aplicada de uma forma inapropriada, onde o contexto da situação seja permitido nas regras do servidor. As regras se encontram em #:small_orange_diamond:regras
・Não pingue a staff, aguarde a resposta

Responda as seguintes indagações:
・ Quem te baniu?
・ Há quanto tempo foi a punição?
・Qual foi o motivo da sua punição informado pelo bot?
・Explique por que a punição foi aplicada de forma indevida: (esse é o seu momento, não terá outra chance! Então, jogue tudo para rolo!)
・Prints são permitidos.


Responda as seguintes indagações e aguarde a resposta de seu unban. Caso queira saber o requesito para ser desbanido, consulte o chat #:small_orange_diamond:unban-kamaitachi
                              ''')
            astaroth = discord.utils.get(member.guild.roles, id=865020156551757864)
            ormenus = discord.utils.get(member.guild.roles, id=865020459501486110)
            acacus = discord.utils.get(member.guild.roles, id=865020484147347457)

            channel = await member.guild.create_text_channel(
                name=str(member.id),
                overwrites={

                    member.guild.default_role: discord.PermissionOverwrite(
                        read_messages=False),

                    member: discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=True,
                        attach_files=True
                    ),

                    ormenus: discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=False,
                        attach_files=False
                    ),

                    acacus: discord.PermissionOverwrite(
                        read_messages=True,
                        send_messages=False,
                        attach_files=False
                    )

                }
            )
            await channel.send(content=member.mention, embed=e)

    @commands.Cog.listener()
    async def on_ready(self):

        print(f"Ready! {self.bot.user}")

        Tasks(self.bot).regsChannelMod.start()
        Tasks(self.bot).updateKaraokeTime.start()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):

        await ctx.reply(content=f"Error: {error}", delete_after=5)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: NewFunctionsPYC.hybridContext, error):

        await ctx.respond(f"Error: {error}", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self,
                         message: discord.Message):

        if message.author == self.bot.user:
            return
        elif message.author.bot:
            return
        elif message.mention_everyone:
            return
        elif not message.guild:
            return
        if "ticket-" in message.channel.name:
            with open(
                    f"./tickets/{message.channel.category.name.removeprefix('ticket ')}/{message.channel.name.removeprefix('ticket-')}.txt",
                    "a",
                    encoding="utf-8"
            ) as f:
                f.write(f"\n{message.author.display_name}: {message.content}")

    @commands.Cog.listener()
    async def on_interaction(self,
                             interaction: discord.Interaction):

        match interaction.to_dict()["type"]:
            case 1:
                return
            case 2:
                return
            case 3:
                match interaction.to_dict()["data"]["component_type"]:
                    case 1:
                        return
                    case 2:
                        if "abrirTicket" in interaction.custom_id:
                            await getattr(custom, f"abrirTicket")(self.bot, interaction)
                        else:
                            try:
                                await getattr(custom, f"{interaction.custom_id}")(self.bot, interaction)
                            except Exception as error:
                                pass
                    case 3:
                        await getattr(custom, f"{interaction.custom_id}")(self.bot, interaction)
                    case 4:
                        return
                    case 5:
                        return
            case 4:
                return
            case 5:
                return


def setup(bot: commands.Bot):
    bot.add_cog(generals(bot))