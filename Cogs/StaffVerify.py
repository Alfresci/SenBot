from unicodedata import name
import nextcord
from nextcord.ext import commands
import nextcord.utils as utils

class StaffVerify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='staffverify')
    async def staffverify(self, ctx):
        channel = await ctx.guild.fetch_channel(995599978602967100)
        await channel.send(f'`🧐` **VERIFICATION REQUEST RECEIVED!**\n{ctx.author.mention} `has requested authorization!` <@&994487740039188541>')

def setup(bot):
    bot.add_cog(StaffVerify(bot))