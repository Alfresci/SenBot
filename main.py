from urllib import response
from nextcord.ext import commands
from nextcord import Intents
import nextcord.ui as ui
import os

my_intents = Intents.default()
my_intents.message_content = True
my_intents.reactions = True

bot = commands.Bot(command_prefix='-', intents = my_intents, help_command=None)

bot.load_extension('Cogs.Moderation')
bot.load_extension('Cogs.Tools')
bot.load_extension('Cogs.Fun')
bot.load_extension('Cogs.ChannelCommands')
bot.load_extension('Cogs.Greetings')
bot.load_extension('Cogs.Recognize')
bot.load_extension('Cogs.HelpCommand')
bot.load_extension('Cogs.Buttons')

@bot.event
async def on_ready():
    bot.add_all_application_commands()
    await bot.sync_application_commands()
    print(f'Logged in as {bot.user.name}.')

bot.run(os.environ['token'])
