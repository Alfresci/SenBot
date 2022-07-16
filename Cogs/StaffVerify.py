from unicodedata import name
from async_timeout import timeout
import nextcord
from nextcord.ext import commands
import nextcord.utils as utils
import nextcord.ui as ui

bot = commands.Bot(command_prefix='-')

class StaffVerify(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.value = None
        self.bot = bot

    @commands.command(name='staffverify')
    async def staffverify(self, ctx):
        channel = await ctx.guild.fetch_channel(995599978602967100)
        await ctx.message.delete()
        author = ctx.author
        role = utils.get(author.guild.roles, name='Crew')

        if ctx.channel != channel:
            await ctx.message.delete()
        else:
            class Options(ui.View):
                @ui.button(label='✔️ Accept', style=nextcord.ButtonStyle.green)
                async def accept(self, button: ui.Button, interaction: nextcord.Interaction):
                    await author.add_roles(role)
                    await interaction.response.send_message(f'Authorized {ctx.author.mention}!')
                    button.disabled = True
                    button.style = nextcord.ButtonStyle.grey
                    await interaction.message.edit(view=self)
                    self.stop()

                @ui.button(label='✖️ Deny', style=nextcord.ButtonStyle.red)
                async def deny(self, button: ui.Button, interaction: nextcord.Interaction):
                    msg = await interaction.response.send_message(f'Denying authorization......')
                    await author.kick()
                    await author.send('You have been kicked from Senpai Station Crew Hub as you were not authorized!')
                    await msg.edit('Denied authorization!')
                    button.disabled = True
                    button.style = nextcord.ButtonStyle.grey
                    await interaction.message.edit(view=self)
                    self.stop()

            view = Options()
            
            await channel.send(f'`🧐` **VERIFICATION REQUEST RECEIVED!**\n{ctx.author.mention} `has requested authorization!`', view=view)

    @commands.command(name='invite')
    @commands.has_any_role('SS', 'COO', 'COM', 'COS', 'Manager', 'Operations Manager')
    async def invite(self, ctx, member: nextcord.Member):
        guild = ctx.message.guild
        verification_channel = await guild.fetch_channel(995300419817459762)
        invite = await verification_channel.create_invite(max_uses=1, max_age=604800)
        await member.send(f'{invite}\nHere is the invite link to Senpai Station Crew Hub.\nDisclaimer - This invite is one-use only and lasts only for 7 days. Please make sure to join the server before 7 days. Also, DO NOT invite anyone to this server. Inviting people into the staff server will result in you getting kicked out of the server.')
        await ctx.message.delete()
        
def setup(bot):
    bot.add_cog(StaffVerify(bot))
