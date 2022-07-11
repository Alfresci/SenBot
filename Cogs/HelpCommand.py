import nextcord
from nextcord.ext import commands
from nextcord import ButtonStyle
from nextcord.ui import Button, View
import json

bot = commands.Bot(command_prefix='-')


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def createhelpembed(self, pagenumber=0, inline=False):
        helpGuide = json.load(open('Cogs\help.json'))

        pageTitle = list(helpGuide)[pagenumber]
        pagenumber = pagenumber % len(list(helpGuide))
        embed = nextcord.Embed(title=pageTitle)
        for key, val in helpGuide[pageTitle].items():
            embed.add_field(name=bot.command_prefix + key, value=val, inline=inline)
            embed.set_footer(text=f'Page {pagenumber + 1} of {len(list(helpGuide))}')
        return embed

    @commands.command(name='help')
    async def help(self, ctx):
        current_page = 0

        async def previous_callback(interaction):
            nonlocal current_page, sent_msg
            current_page -= 1
            await sent_msg.edit(embed=self.createhelpembed(pagenumber=current_page), view=myview)

        async def next_callback(interaction):
            nonlocal current_page, sent_msg
            current_page += 1
            await sent_msg.edit(embed=self.createhelpembed(pagenumber=current_page), view=myview)

        nextPage = Button(label='►', style=ButtonStyle.red)
        nextPage.callback = next_callback
        previousPage = Button(label='◄', style=ButtonStyle.red)
        previousPage.callback = previous_callback

        myview = View(timeout=180)
        myview.add_item(previousPage)
        myview.add_item(nextPage)
        sent_msg = await ctx.send(embed=self.createhelpembed(pagenumber=0), view=myview)


def setup(bot):
    bot.add_cog(Help(bot))
