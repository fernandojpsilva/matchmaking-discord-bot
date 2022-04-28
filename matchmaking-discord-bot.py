import discord
import cassiopeia as cass

TOKEN = ''
cass.set_riot_api_key('')

client = discord.Client()


def getSummonerRank(name):
    rank = cass.get_summoner(name=name, region="EUW").league_entries.fives
    return rank


def getSummoner(name):
    summoner = cass.get_summoner(name=name, region="EUW")
    return summoner


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
        if user_message.lower().startswith("!lol"):
            name = user_message.split(" ")[1]
            summoner = getSummoner(name)
            summoner_rank = getSummonerRank(name)
            await message.channel.send(f'{summoner.name} - Nível {summoner.level} - {summoner_rank.league.tier}'
                                       f' {summoner_rank.division} ({summoner_rank.league_points} LP)')
            return


client.run(TOKEN)
