from nextcord.ext import commands


class Recognize(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

    @commands.command(name = 'recognize')
    @commands.is_owner()
    async def recognize(self, ctx):
        await ctx.reply('The owner is recognized! <:tada:988068624721928213>')

    @recognize.error
    async def recognize_error(self, ctx : commands.Context, error : commands.NotOwner):
        if isinstance(error, commands.NotOwner):
            await ctx.reply('You are not the owner <:neutral_face:987969729132118076>')


def setup(bot):
    bot.add_cog(Recognize(bot))