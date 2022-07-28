from urllib import response
import nextcord
from nextcord.ext import commands
from nextcord import Intents
import nextcord.ui as ui

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
bot.load_extension('Cogs.StaffVerify')
bot.load_extension('Cogs.Error')


guild_id = [927811764895227945, 994484729917210646]  

class Application(nextcord.ui.Modal):
        def __init__(self):
            super().__init__(title='Staff Application', timeout= 10 * 60 #10 minutes
            )

            self.name = ui.TextInput(
                label='Your Discord Username with Discriminator',
                placeholder='YourUsername#0000',
                min_length=6,
                max_length=20,
            )
            self.add_item(self.name)
            
            self.id = ui.TextInput(
                label='Your Discord ID',
                placeholder='Your ID',
                min_length=18,
                max_length=20,
            )
            self.add_item(self.id)
            
            self.description = ui.TextInput(
                label='Give us a brief description of yourself.',
                placeholder='Describe yourself',
                style=nextcord.TextInputStyle.short,
            )
            self.add_item(self.description)

            self.question1 = ui.TextInput(
                label='What is your real name? (It will not be disclosed to anyone)',
                placeholder='Your name',
                min_length=1,
                max_length=20,
            )
            self.add_item(self.question1)
            
            self.question2 = ui.TextInput(
                label='Your age',
                placeholder='Age',
                min_length=1,
                max_length=2,
            )
            self.add_item(self.question2)

            self.question3 = ui.TextInput(
                label='What do you want to apply for staff?',
                style=nextcord.TextInputStyle.short,
                placeholder='Answer',
            )
            self.add_item(self.question3)

            self.question4 = ui.TextInput(
                label='List your previous experiences',
                style=nextcord.TextInputStyle.short,
                placeholder='Answer',
            )
            self.add_item(self.question4)

            self.question5 = ui.TextInput(
                label='Why should we select you?',
                style=nextcord.TextInputStyle.short,
                placeholder='Answer',
            )
            self.add_item(self.question5)

            self.question6 = ui.TextInput(
                label='What are your strengths and weaknesses?',
                style=nextcord.TextInputStyle.paragraph,
                placeholder='Answer'
            )
            self.add_item(self.question6)

        async def callback(self, interaction: nextcord.Interaction) -> None:
            response = nextcord.Embed(title=f"{interaction.user.name}'s Staff Application", 
            description=f"**{self.name.label}**\n**Ans - **{self.name.value}\n**{self.id.label}**\n**Ans - **{self.id.value}\n**{self.description.label}**\n**Ans - **{self.description.value}")

            response.add_field(f'**{self.question1.label}**\n**Ans - **{self.question1.value}')
            response.add_field(f'**{self.question2.label}**\n**Ans - **{self.question2.value}')
            response.add_field(f'**{self.question3.label}**\n**Ans - **{self.question3.value}')
            response.add_field(f'**{self.question4.label}**\n**Ans - **{self.question4.value}')
            response.add_field(f'**{self.question5.label}**\n**Ans - **{self.question5.value}')
            response.add_field(f'**{self.question6.label}**\n**Ans - **{self.question6.value}')
    

@bot.slash_command(name='apply', description='Apply for the Staff Team', guild_ids=guild_id)
async def apply(interaction: nextcord.Interaction):
    modal = Application()
    applications_chanel = await interaction.guild.fetch_channel(1000624490541240390)
    await applications_chanel.send(embed = response)
    await interaction.response.send_message('Application Sent!', ephemeral=True)


@bot.event
async def on_ready():
    bot.add_all_application_commands()
    await bot.sync_application_commands()
    print(f'Logged in as {bot.user.name}.')


bot.run(os.environ['token'])
