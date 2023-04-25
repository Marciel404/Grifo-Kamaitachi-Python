import time
import discord
from discord.ext import commands


class ping(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        start_time: time = time.time()

        Ping: int = round(self.bot.latency * 1000)

        end_time: time = time.time()

        p4: discord.Embed = discord.Embed(
            title='Ping',
            description=f'Ping: {Ping}ms\nAPI: {round((end_time - start_time) * 1000)}ms',
        )

        await ctx.reply(embed=p4)


def setup(bot: commands.Bot):
    bot.add_cog(ping(bot))
