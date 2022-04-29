import discord
import cassiopeia as cass

TOKEN = ''
cass.set_riot_api_key('')

client = discord.Client()


def getSummonerString(user_message):
    # Split game from summoner name, strip summoner name for
    # names with multiple words
    split_message = user_message.split(" ", 1)
    name = split_message[1].strip()
    summoner = getSummoner(name)
    summoner_rank = getSummonerRank(name)

    if summoner is not False:
        print(summoner)
        if summoner_rank is not False:
            summoner_string = f'{summoner.name} - Nível {summoner.level} - {summoner_rank.league.tier} ' \
                              f'{summoner_rank.division} ({summoner_rank.league_points} LP)'
            return summoner_string
        else:
            summoner_string = f'{summoner.name} - Nível {summoner.level} - Unranked'
            return summoner_string
    else:
        print("tou aqui")
        summoner_string = 'Quem? :banana:'
        return summoner_string


def isLolSummonerRequest(msg):
    if msg.startswith("!lol "):
        return True
    else:
        return False


def getSummonerRank(name):
    try:
        rank = cass.get_summoner(name=name, region="EUW").league_entries.fives
        return rank
    except Exception as err:
        return False


def getSummoner(name):
    # Returns summoner if exists, or false otherwise
    try:
        summoner = cass.get_summoner(name=name, region="EUW")
        if summoner.id:
            return summoner
        else:
            return False
    except Exception as err:
        return False


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content).lower()
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    if message.channel.name == 'testing':
        if isLolSummonerRequest(user_message):
            await message.channel.send(getSummonerString(user_message))
            return


client.run(TOKEN)
