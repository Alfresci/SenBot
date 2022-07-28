from distutils.log import error
import nextcord
from nextcord.ext import commands

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @error
    async def error(self, ctx,error: commands.CommandNotFound):
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.delete()

def setup(bot):
    bot.add_cog(Error(bot))