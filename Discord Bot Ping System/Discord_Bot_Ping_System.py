import discord
import random
from discord import app_commands
from datetime import datetime, timedelta


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        await self.tree.sync(guild=discord.Object(id=335903736142626827))
        await self.tree.sync()
        self.tree.copy_global_to(guild=discord.Object(id=335903736142626827))

# Time of the last embed message
last_embed_time = None

intents = discord.Intents.default()
client = MyClient(intents=intents)


EmbedFooter = 'Serperior Pinging Services | Version 2.1.3 | -Snivy Films'

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your discussions"))
    print(f'{client} has successfully connected')

# List of customizable messages
with open("messages.txt", "r") as f:
    messages = [line.strip() for line in f]

@client.event
async def on_message(message):
    global last_embed_time
    if message.mentions:
        # Check if 5 minutes have passed since the last embed message
        if last_embed_time is None or datetime.now() - last_embed_time > timedelta(minutes=2):
            response = random.choice(messages)
            embed = discord.Embed(title="Ping Trigger", description=f"{message.author.mention} - {response}", color=0x00ffbd)
            embed.set_footer(text= EmbedFooter)
            await message.channel.send(embed=embed)
            last_embed_time = datetime.now()
@client.tree.command(name = "add-message", description = "Add a new message to the ping trigger")
async def self(interaction: discord.Interaction, message:str):
    try:
        with open("messages.txt", "a", encoding='utf-8') as f:
            f.write(message + "\n")
        embed = discord.Embed(title="New Ping Trigger Message", description=f"{interaction.user.mention} - You have sucessfully added a new message: {message}", color=0x00ffbd)
        embed.set_footer(text= EmbedFooter)
        await interaction.response.send_message(embed=embed)
        with open("messages.txt", "r") as f:
            messages = [line.strip() for line in f]
    except UnicodeEncodeError:
        embed = discord.Embed(title="Error Code 1", description="The message could not be added because it is not in the UTF-8 format. Please try again. If you are sure that the message is in UTF-8 format please contact the bot handler.", color=0xff0000)
        embed.set_footer(text= EmbedFooter)
        await interaction.response.send_message(embed=embed)

@client.tree.command(name="message-count", description="Get the amount of messages for the ping trigger")
async def self(interaction: discord.Interaction):
    try:
        with open("messages.txt", "r") as f:
            messages = [line.strip() for line in f]
            count = len(messages)
            embed = discord.Embed(title="Message Count", description=f"{interaction.user.mention} - There are {count} messages in the ping trigger messages file", color=0x00ffbd)
            embed.set_footer(text=EmbedFooter)
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="Error Code 2", description=f"Something has gone critically wrong. Contact the bot master immediately. Include what you were doing to cause the error to occur", color=0xff0000)
        embed.set_footer(text=EmbedFooter)
        await interaction.response.send_message(embed=embed)

client.run("MTEwMDc5MjEwNDEyNjUyOTU4OA.GO9LBB.u6lQwHDrzGpuQ7FjP1IwBfI0hppcfROGWfClf8")