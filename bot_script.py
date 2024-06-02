import time
import os
import discord

# regionEnvironment Variables
my_bot_token = os.getenv('hym_token')
if not my_bot_token:
    print('error, la variable no se cargo sastifactoriamente')

indecent_words = [
    "Porno", "porno",
    "xxx"
]
user_messages = {}
TIME_WINDOW = 7
umbral = 5
channel_id = 1246638973271670886
# endregion


intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} - {client.user.id}')
    print('=-=-=-=-=-=')


@client.event
async def on_message(message):
    if message.author.bot:
        content = message.content.lower()
        if any(word in content for word in indecent_words):
            guild = message.guild
            bot_indecent = guild.get_member(message.author.id)
            if bot_indecent:
                try:
                    await guild.kick(bot_indecent)
                    channel = guild.get_channel(channel_id)
                    if channel:
                        await channel.send(f'Bot {message.author.name} fue expulsado por enviar spam')
                except Exception as e:
                    print(e)
    now = time.time()
    user_id = message.author.id
    if user_id not in user_messages:
        user_messages[user_id] = []
    user_messages[user_id] = [timestamp for timestamp in user_messages[user_id] if now - timestamp < TIME_WINDOW]
    user_messages[user_id].append(now)

    if len(user_messages[user_id]) > umbral:
        guild = message.guild
        bot_indecent = guild.get_member(message.author.id)
        if bot_indecent:
            try:
                await message.channel.purge(limit=umbral, check=lambda m: m.author == bot_indecent)
                await guild.kick(bot_indecent)
                channel = guild.get_channel(channel_id)
                if channel:
                    await channel.send(f'Usuario {bot_indecent.name} fue expulsado por enviar spam')
            except Exception as e:
                print(e)
        user_messages[user_id] = []


client.run(f'{my_bot_token}')
