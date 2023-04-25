import json
from discord import Embed, Message
from discord.ext import commands
from checks.cargos import has_roles
from utils.loader import configData


class anunciarEvento(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="anunciar_evento",
        description="Envia a mensagem anunciando o evento",
        aliases=["anun_evento"]
    )
    @has_roles(
        configData["roles"]["staff"]["staff1"],
        configData["roles"]["staff"]["staff2"],
        configData["roles"]["equipe_evento"],
    )
    async def anunciar_evento(self, ctx: commands.Context, *, json_embed: str = None):

        if json_embed is None:

            mm = await ctx.reply("Envie o json da embed")

            def check(m: Message):
                return m.content and m.author == ctx.author

            msg = await self.bot.wait_for("message", check=check)

            je = json.loads(msg.content)
            content = ""
            if "content" in je:
                content = je["content"]

            e = Embed().from_dict(je)

            await msg.delete()
            await mm.delete()
            await ctx.send("Prontinho ;), anunciado")
            return await ctx.guild.get_channel(configData["channels"]["anun_evento"]).send(
                content=content,
                embed=e
            )

        je = json.loads(json_embed)
        content = ""
        if "content" in je:
            content = je["content"]

        e = Embed().from_dict(je)

        await ctx.send("Prontinho ;), anunciado")
        await ctx.guild.get_channel(configData["channels"]["anun_evento"]).send(
            content=content,
            embed=e
        )


def setup(bot: commands.Bot):
    bot.add_cog(anunciarEvento(bot))