import nextcord
from nextcord.ext import commands


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(
                f"Welcome to Alpha's World {member.mention}!\nDon't forget to read the rules in <#945309609420275742>.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(status=nextcord.Status.idle,
                                       activity=nextcord.Game("Watching over Senpai Station."))

    @commands.command(name='setactivity', aliases=['sa'])
    @commands.has_role('SS')
    async def setactivity(self, ctx, status: str):
        await self.bot.change_presence(activity=nextcord.Game(status))
        await ctx.send(f'Activity changed to **{status}**!')


def setup(bot):
    bot.add_cog(Greetings(bot))
