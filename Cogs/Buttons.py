from nextcord.ext import commands
from nextcord import ButtonStyle
import nextcord.ui as ui


class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='support')
    async def support(self, ctx):
        hi = ui.Button(label="Alpha's World", style=ButtonStyle.red)
        redirect = ui.Button(label='Redirect to support server', style=ButtonStyle.red,
                          url='https://discord.gg/F2tkagb7Br')

        async def hi_callback(interaction):
            await interaction.response.send_message('discord.gg/GmEwppZrK5')

        hi.callback = hi_callback

        myview = ui.View(timeout=180)
        myview.add_item(hi)
        myview.add_item(redirect)

        await ctx.send('Your command reply.', view=myview)


def setup(bot):
    bot.add_cog(Buttons(bot))
