import json

import discord
from discord import Embed
from discord.ext import commands
from checks.cargos import has_roles
from utils.loader import configData


class embed(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @has_roles(
        configData["roles"]["staff"]["staff1"],
        configData["roles"]["staff"]["staff2"],
        configData["roles"]["capitaes_evento"],
        configData["roles"]["capitaes_karaoke"],
        configData["roles"]["capitaes_arte"],
        configData["roles"]["capitaes_poem"]
    )
    async def embed(self, ctx: commands.Context, canal: discord.TextChannel, json_embed: str = None):

        if json_embed is None:

            await ctx.message.delete()

            m = await ctx.send("Envie o json da embed")

            def check(m: discord.Message):
                return m.content and m.author == ctx.author

            msg = await self.bot.wait_for("message", check=check)

            je = json.loads(msg.content)
            content = ""
            if "content" in je:
                content = je["content"]

            e = discord.Embed().from_dict(je)

            await m.delete()
            await msg.delete()
            await canal.send(content=content, embed=e)
            return await ctx.channel.send(content=f"Embed enviada no canal {canal.mention}", delete_after=5)

        je = json.loads(json_embed)
        content = ""
        if "content" in je:
            content = je["content"]

        e = Embed().from_dict(je)

        await ctx.message.delete()
        await canal.send(content=content, embed=e)
        await ctx.channel.send(content=f"Embed enviada no canal {canal.mention}", delete_after=5)

def setup(bot: commands.Bot):
    bot.add_cog(embed(bot))