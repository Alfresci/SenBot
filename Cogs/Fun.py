from random import randint
import nextcord
from nextcord.ext import commands
import nextcord.ui as ui


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mystery')
    async def test(self, ctx):

        async def dropdown_callback(interaction):
            for value in dropdown.values:
                await ctx.send(value)
        option1 = nextcord.SelectOption(label='A mystery option', value='Get rickrolled!', description='What might this be?', emoji='🤔')
        option2 = nextcord.SelectOption(label='Just your normal option', value='Hello!', description='A test option', emoji='👋')
        dropdown = ui.Select(placeholder='Your options!', options=[option1,option2], max_values=1)
        dropdown.callback = dropdown_callback
        myview = ui.View(timeout=180)
        myview.add_item(dropdown)
        await ctx.send('Your options are given below!', view=myview)

    @commands.command(name='vixen')
    async def vixen(self, ctx):
        await ctx.send('<@750034738751733883>')
        await ctx.message.delete()

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.reply('Pong!')

    @commands.command(name='die', aliases=['ded'])
    async def die(self, ctx):
        await ctx.reply('https://tenor.com/view/jim-carrey-stoned-frozen-dead-inside-gif-15445047')

    @commands.command(name='greet')
    async def greet(self, ctx, member: nextcord.Member):
        await ctx.send(f'Hello {member.mention}!')
        await ctx.message.delete()

    @commands.command(name='bean')
    @commands.has_role('Level 1')
    async def bean(self, ctx, member: nextcord.Member):
        await ctx.send(
            f'{member.mention} has been beaned!\nhttps://tenor.com/view/dance-bean-dancing-cute-funny-gif-21992996')
        await ctx.message.delete()

    @bean.error
    async def bean_error(self, ctx: commands.Context, error: commands.MissingAnyRole):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.message.delete()
            await ctx.send(f'{ctx.author.mention} is a fool <:joy:>')

    @commands.group(name='guessthenumber', aliases = ['gtn'])
    async def guessthenumber(self, ctx):
        embed = nextcord.Embed(title='**GUESS THE NUMBER**', description='A random number is selected between 1 to 100. Guess the correct number to win the game! Use `-gtn ans [your number here]` to answer. (Do not include the brackets)')
        embed.add_field(value='Use `-gtn hint` to get a hint <:wink:>', inline=False)
        await ctx.send(embed=embed)

    @guessthenumber.command(name='ans')
    async def ans(self, ctx, number: int):
        selected_number = randint(a=0, b=100)
        if selected_number == number:
            await ctx.send(f'{ctx.author.mention} has guessed correctly!')
        else:
            await ctx.send('Wrong number :(. Try again.')
    '''
    @guessthenumber.command(name='hint')
    async def hint(self, ctx):
        hint1 = selected_number + 20
        hint2 = selected_number - 20
        await ctx.send(f'The number is between {hint1} and {hint2}.')
    '''

def setup(bot, **kwargs):
    bot.add_cog(Fun(bot, **kwargs))
