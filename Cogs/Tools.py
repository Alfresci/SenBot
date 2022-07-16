from email import message
from unicodedata import name
import nextcord
from nextcord.ext import commands
import asyncio
import nextcord.utils as utils


class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name='dm', description='DMs a user', guild_ids=[927811764895227945, 994484729917210646])
    async def dm(self, interaction: nextcord.Interaction, member: nextcord.Member, message: str):
        await member.send(f'**Message from {interaction.user.mention}:**\n{message}')
        await interaction.response.send_message(f'Sent message to {member.mention}', ephemeral = True)
    
    @commands.command(name='managenickname', aliases = ['mn'])
    @commands.has_any_role('Admin', 'Manager')
    async def managenickname(self, ctx, member: nextcord.Member, *, nick: str):
        await member.edit(nick=nick)
        await ctx.send(f"{member.mention}'s nickname has been changed to {nick}!")
    
    @commands.command(name='poll')
    @commands.has_any_role('Events Team', 'Support Team', 'Development Team')
    async def poll(self, ctx, question: str, option1: str = None, option2: str = None):
        embed = nextcord.Embed(title=f'**{question}**',
                               description=f'<:one:988434351614218270> {option1}\n<:two:988434728090734623> {option2}')
        embed.set_footer(text=f'Poll created by {ctx.author.name}')
        msg = await ctx.send(embed=embed)
        e1 = '1\uFE0F\u20E3'
        e2 = '2\uFE0F\u20E3'
        await msg.add_reaction(e1)
        await msg.add_reaction(e2)

    @commands.command(name='addcrew', aliases=['ac'])
    @commands.has_any_role('Manager', 'Team Leader')
    async def addcrew(self, ctx, member: nextcord.Member):
        role = nextcord.utils.get(member.guild.roles, name='Helper')
        await member.add_roles(role)
        embed = nextcord.Embed(title=f'Hired {member}!', description=f'{member.mention} Welcome to the staff team!')
        await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=2)

    @addcrew.error
    async def addcrew_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0XFF0000)
            await ctx.reply(embed=embed)

    @commands.command(name='remcrew', aliases=['rc'])
    @commands.has_any_role('Manager', 'Team Leader')
    async def remcrew(self, ctx, member: nextcord.Member):
        role = nextcord.utils.get(member.guild.roles, name='Helper')
        await member.remove_roles(role)
        embed = nextcord.Embed(title=f'Fired {member}!',
                               description=f'{member.mention} has been fired from the staff team!')
        await ctx.send(embed=embed)
        await member.send(f'You were fired from the staff team in {ctx.guild.name}.')
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=2)

    @remcrew.error
    async def remcrew_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0XFF0000)
            await ctx.reply(embed=embed)

    @commands.command(name='lock')
    @commands.has_any_role('Sr. Moderator', 'Admin', 'Manager')
    async def lock(self, ctx, channel: nextcord.TextChannel = None):
        channel = ctx.channel or channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('Channel locked!')

    @lock.error
    async def lock_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.reply(embed=embed)
            return

    @commands.command(name='unlock')
    @commands.has_any_role('Sr. Moderator', 'Admin', 'Manager')
    async def unlock(self, ctx, channel: nextcord.TextChannel = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('Channel unlocked!')

    @unlock.error
    async def unlocks_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command(name='slowmode', aliases=['slow', 'sm'])
    @commands.has_any_role('Moderation Team', 'Manager')
    async def slowmode(self, ctx, time: int):
        await ctx.channel.edit(slowmode_delay=time)
        await ctx.send(f'Slowmode set to {time} seconds!')

    @slowmode.error
    async def slowmode_error(self, ctx: commands.Context, error: commands.MissingRole):
        if isinstance(error, commands.MissingRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command(name='roleid')
    async def roleid(self, ctx, role_name : str):
        role = utils.get(ctx.author.guild.roles, name=role_name)
        role_id = role.id
        await ctx.send(f'The roles id for {role_name} is {role_id}.')
    
    @commands.command(name='rolemembers')
    async def rolemembers(self, ctx, role_name : str):
        role = utils.get(ctx.guild.roles, name=role_name)
        role_members = role.members
        await ctx.send(f'The members for this role are: \n{role_members}')
    
    @commands.command(name='role')
    @commands.has_any_role('Manager', 'Team Leader')
    async def role(self, ctx, member: nextcord.Member, role_name: str):
        role = utils.get(member.guild.roles, name=role_name)
        author = ctx.author
        author_top_role = author.top_role
        top_role = utils.get(member.guild.roles, name=author_top_role.name)
        role_position = role.position
        top_role_position = top_role.position
        if role_position > top_role_position:
            await ctx.send(f'You are not authorized to give this role to {member.mention}!')
        elif role_position < top_role_position:
            await member.add_roles(role)
            embed = nextcord.Embed(title='Roles Changed!', description=f'{role_name} added to {member.mention}')
            await ctx.send(embed=embed)
        elif role_position == top_role_position:
            await ctx.send(f'You cannot give your own role to others. Ask a user with a higher role to do so.')
        else:
            await ctx.send("Hm..... The command doesn't seem to work <:thinking:>")

    @commands.command(name='removerole', aliases=['remrole'])
    @commands.has_any_role('Admin', 'Manager')
    async def removerole(self, ctx, member: nextcord.Member, role_name: str):
        role = utils.get(member.guild.roles, name=role_name)
        author = ctx.author
        author_top_role = author.top_role
        top_role = utils.get(member.guild.roles, name=author_top_role.name)
        role_position = role.position
        top_role_position = top_role.position
        if role_position > top_role_position:
            await ctx.send(f'You are not authorized to remove the role from {member.mention}!')
        elif role_position < top_role_position:
            await member.remove_roles(role)
            embed = nextcord.Embed(title='Roles Changed!', description=f'{role} removed from {member.mention}!')
            await ctx.send(embed=embed)
        elif role_position == top_role_position:
            await ctx.send(f'You cannot remove the role. Ask a user with a higher role to do so.')
        else:
             await ctx.send("Hm..... The command doesn't seem to work <:thinking:>")


    @commands.command(name='nuke')
    @commands.has_any_role('SS', 'COO', 'COS')
    async def nuke(self, ctx):
        channel = await ctx.channel.clone(name=f'{ctx.channel.name}')
        await ctx.channel.delete()
        await channel.send(f'Nuked by `{ctx.author.name}`.')

    @nuke.error
    async def nuke_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.group(name='space', aliases=['spc'])
    async def space(self, ctx):
        await ctx.send('This is the testspace command. Sub-Commands are: Create, Add, Close')

    @space.command(name='create')
    async def create(self, ctx, *, reason='No reason provided'):
        guild = ctx.message.guild
        user = ctx.message.author
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            ctx.message.author: nextcord.PermissionOverwrite(view_channel=True)
        }

        channel = await guild.create_text_channel(name=f'{ctx.author.name}', overwrites=overwrites, reason=reason,
                                                  topic=f'Bot testing space for {ctx.author.name}')
        await channel.send(f'{user.mention}')
        await asyncio.sleep(2)
        await channel.purge(limit=1)
        embed1 = nextcord.Embed(title='Reason:', description=f'{reason}')
        await channel.send(embed=embed1)
        embed = nextcord.Embed(title='Channel Created!', description='Your channel has been created!')
        await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=3)

    @space.command(name='add')
    async def add(self, ctx, member: nextcord.Member):
        channel = ctx.channel
        overwrite = nextcord.PermissionOverwrite()
        overwrite.read_messages = True
        overwrite.send_messages = True
        overwrite.view_channel = True
        await channel.set_permissions(member, overwrite=overwrite)
        await ctx.send(f'{member.name} has been added to the space!')

    @space.command(name='remove')
    async def remove(self, ctx, member: nextcord.Member):
        channel = ctx.channel
        overwrite = nextcord.PermissionOverwrite()
        overwrite.read_messages = False
        overwrite.send_messages = False
        overwrite.view_channel = False
        await channel.set_permissions(member, overwrite=overwrite)
        await ctx.send(f'{member.name} has been removed from the space!')
    
    @space.command(name='close')
    @commands.has_role('Support Team')
    async def close(self, ctx):
        channel = ctx.channel
        await ctx.send('Closing space.....')
        await channel.delete()

    @commands.command(name='task')
    @commands.has_any_role('Manager', 'Team Leader', 'Deputy Team Leader')
    async def tasks(self, ctx, member: nextcord.Member, *, task: str):
        await ctx.send(f'{member.mention} has been assigned a task: {task}!')

    @tasks.error
    async def task_error(self, ctx: commands.Context, error: commands.MissingPermissions):
        if isinstance(error, commands.MissingPermissions):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.send(embed=embed)
            return

    @commands.command(name='clear', aliases=['c', 'purge'])
    @commands.has_any_role('Moderation Team', 'Manager')
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount + 1)

    @clear.error
    async def clear_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            embed = nextcord.Embed(title='ERROR!', description='You are missing the permissions to use this command!',
                                   color=0xFF0000)
            await ctx.send(embed=embed)
            return


def setup(bot, **kwargs):
    bot.add_cog(Tools(bot, **kwargs))
