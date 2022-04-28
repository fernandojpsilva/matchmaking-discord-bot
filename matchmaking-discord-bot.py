import discord

TOKEN = ''

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'testing':
        if user_message.lower() == 'hello':
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == 'bye':
            await message.channel.send(f'See you later {username}')
            return
        elif user_message.lower() == '!random':
            response = f'Random'
            await message.channel.send(response)
            return

    if user_message.lower() == "!anywhere":
        await message.channel.send("Anywhere")
        return

client.run(TOKEN)
