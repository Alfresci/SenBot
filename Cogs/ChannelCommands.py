import nextcord
from nextcord.ext import commands
import asyncio


class ChannelEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='channelname', aliases=['cn', 'name'])
    @commands.has_any_role('Admin', 'Head Admin', 'Manager')
    async def channelname(self, ctx, *, name: str):
        await ctx.channel.edit(name=name)
        await ctx.reply(f'Channel name changed to {name}!')
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=2)

    @channelname.error
    async def channelname_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.reply(embed=embed)
            return

    @commands.command(name='channeldescription', aliases=['cd', 'channeldes', 'des'])
    @commands.has_any_role('Admin', 'Head Admin', 'Manager')
    async def channeldescription(self, ctx, *, description: str):
        await ctx.channel.edit(topic=description)
        await ctx.reply(f'Channel description changed to "{description}"!')
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=2)

    @channeldescription.error
    async def channeldescription_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.reply(embed=embed)
            return


def setup(bot, **kwargs):
    bot.add_cog(ChannelEdit(bot, **kwargs))