import discord
import responses
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


def run_discord_bot():
    TOKEN = 'MTA0MjAzNjgzMzc3MDU0OTMyOA.GXqFpH.GQ3TfHJXLLzTkBezeToyD4eNmYz5xAoJDumNW4'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    @bot.tree.command(name="hello")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}! This is slash command!")

    @bot.tree.command(name="say")
    @app_commands.describe(thing_to_say="What should i say?")
    async def say(interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
