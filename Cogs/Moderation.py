import json
import nextcord
from nextcord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open('reports.json', encoding='utf-8') as f:
            try:
                self.report = json.load(f)
            except ValueError:
                self.report = {'members': []}
    
    @commands.command(name='kick')
    @commands.has_any_role('Admin','Operations Manager', 'COO', 'COS', 'COM', 'SS')
    async def kick(self, ctx, member: nextcord.Member, reason: str):
        await member.kick(reason=reason)
        em = nextcord.Embed(title='User kicked!', description=f'{member} has been kicked!', color=0xFF0000)
        em.add_field(name='Reason:', value=f'{reason}')
        await ctx.send(embed=em)
        await member.send(f'You have kicked from {member.guild} because of {reason}.')

    @kick.error
    async def kick_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command(name='ban')
    @commands.has_any_role('Admin', 'Operations Manager')
    async def ban(self, ctx, member: nextcord.Member, *, reason='No reason provided'):
        await member.ban(reason=reason)
        em = nextcord.Embed(title='User banned!', description=f'{member} has been banned!\n{reason}', color=0xFF0000)
        await ctx.send(embed=em)
        await member.send(f'You have banned from {member.guild} because of {reason}.')

    @ban.error
    async def ban_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command(name='warn')
    @commands.has_any_role('Moderation Team', 'Operations Manager', 'COO', 'COS', 'COM', 'SS')
    async def warn(self, ctx, member: nextcord.Member, *, reason: str):
        author = ctx.author
        if member == author:
            await ctx.send('You cannot warn yourself!')
        if not reason:
            await ctx.send("Please provide a reason")
            return
        reason = ''.join(reason)
        await ctx.send(f'**{member.mention} has been warned by {author.mention}.**')
        await member.send(f'You have been warned in **{ctx.guild.name}**.'
                          f'Reason - **{reason}**')

        for current_user in self.report['members']:
            if current_user['name'] == member.name:
                current_user['reasons'].append(reason)
                break
            else:
                self.report['members'].append({
                    'name': member.name,
                    'reasons': [reason, ]
                })
            with open('Cogs/reports.json', 'w+') as f:
                json.dump(self.report, f)

            with open('Cogs/reports.json', 'w+') as f:
                json.dump(self.report, f)
            if len(self.report['members']) >= 7:
                await member.kick(reason='You reached 7 warnings!')
                await member.send(f'You have been kicked from {ctx.guild.name} because you have reached 7 warnings!')

    @warn.error
    async def warn_error(self, ctx: commands.Context, error: commands.MissingRole):
        if isinstance(error, commands.MissingRole):
            embed = nextcord.Embed(title='ERROR!',
                                   description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command(name='warnings', aliases=['warns'])
    @commands.has_any_role('Moderation Team', 'Operations Manager', 'COO', 'COS', 'COM', 'SS')
    async def warnings(self, ctx, member: nextcord.Member):
        for current_user in self.report['members']:
            if member.name == current_user['name']:
                await ctx.send(
                    f"**{member.name} has been reported {len(current_user['reasons'])} times : {','.join(current_user['reasons'])}**")
                break
            else:
                await ctx.send(f"**{member.name} has never been reported**")

    @commands.command(name='clearwarns', aliases=['warnsclear', 'cw'])
    @commands.has_any_role('Admin', 'Operations Manager')
    async def clearwarns(self, ctx, member: nextcord.Member):
        for current_user in self.report['members']:
            if current_user['name'] == member.name:
                current_user['reasons'].pop()
                await ctx.send(f"**{member.mention}'s warns have been cleared!**")
                break
            else:
                await ctx.send(f'**{member} has never been warned!**')

    @clearwarns.error
    async def clearwarns_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!',
                                   description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command(name='clearallwarns', aliases=['cwall'])
    @commands.has_any_role('COO', 'COS', 'COM', 'SS')
    async def clearallwarns(self, ctx):
        self.report.clear()
        await ctx.send('All warns have been cleared!')


def setup(bot):
    bot.add_cog(Moderation(bot))
