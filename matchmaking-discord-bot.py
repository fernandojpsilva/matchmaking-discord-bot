import discord
import cassiopeia as cass

TOKEN = ''
cass.set_riot_api_key('')

client = discord.Client()


def getBlueTeam(match):
    blue_summoners_list = []

    for item in match.blue_team.participants:
        summoner_name = item.summoner.name
        rank = getSummonerRank(summoner_name)
        blue_summoners_list.append([summoner_name, rank.league.tier, rank.division, rank.league_points])

    return blue_summoners_list


def getRedTeam(match):
    red_summoners_list = []

    for item in match.red_team.participants:
        summoner_name = item.summoner.name
        rank = getSummonerRank(summoner_name)
        red_summoners_list.append([summoner_name, rank.league.tier, rank.division, rank.league_points])

    return red_summoners_list


def generateMatchString(summoner_name):
    match = getCurrentMatch(summoner_name)
    blue_summoners_list = getBlueTeam(match)
    red_summoners_list = getRedTeam(match)
    print(blue_summoners_list)
    print(red_summoners_list)
    return blue_summoners_list


def getCurrentMatch(summoner_name):
    summoner = getSummoner(summoner_name)
    try:
        match = summoner.current_match
        return match
    except Exception as err:
        error = 'Not in game'
        return error


def generateSummonerString(summoner_name):
    summoner = getSummoner(summoner_name)
    summoner_rank = getSummonerRank(summoner_name)

    if summoner is not False:
        if summoner_rank is not False:
            wr = str(round(summoner_rank.wins/(summoner_rank.wins+summoner_rank.losses)*100, 2))
            played = summoner_rank.wins+summoner_rank.losses
            embed = discord.Embed(title=f'{summoner.name} - Nível {summoner.level}',
                                  description=f'**{summoner_rank.league.tier} {summoner_rank.division} '
                                              f'({summoner_rank.league_points} LP) - {wr}% WR ({played} Jogos)**\n\n'
                                              f'**[OPGG](https://euw.op.gg/summoners/euw/{summoner_name})**',
                                  colour=discord.Colour.blue())
            return embed
        else:
            embed = discord.Embed(title=f'{summoner.name} - Nível {summoner.level}',
                                  description=f'Unranked\n\n'
                                              f'**[OPGG](https://euw.op.gg/summoners/euw/{summoner_name})**',
                                  colour=discord.Colour.blue())
            return embed
    else:
        summoner_string = 'Quem? :heheboy:'
        return summoner_string


def requestType(msg):
    if msg.startswith('!lol '):
        return 'lol_summoner'
    elif msg.startswith('!lolgame'):
        return 'lolgame'
    else:
        return False


# Split game from summoner name, strip summoner name for
# names with multiple words
def extractNameFromMessage(user_message):
    split_message = user_message.split(" ", 1)
    name = split_message[1].strip()
    return name


def getSummonerRank(name):
    try:
        rank = cass.get_summoner(name=name, region='EUW').league_entries.fives
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
        if requestType(user_message) == 'lol_summoner':
            summoner_name = extractNameFromMessage(user_message)
            await message.channel.send(embed=generateSummonerString(summoner_name))
            return
        elif requestType(user_message) == 'lolgame':
            await message.channel.send('Ora espera lá um segundinho...')
            summoner_name = extractNameFromMessage(user_message)
            await message.channel.send(generateMatchString(summoner_name))
            return

client.run(TOKEN)
