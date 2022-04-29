import discord
import cassiopeia as cass
from table2ascii import table2ascii as t2a, PresetStyle

TOKEN = ''
cass.set_riot_api_key('')

client = discord.Client()


def getBlueTeam(match):
    blue_summoners_list = []

    for item in match.blue_team.participants:
        summoner_name = item.summoner.name
        champion = item.champion.name
        rank = getSummonerRank(summoner_name)
        wr = str(round(rank.wins / (rank.wins + rank.losses) * 100, 2))
        blue_summoners_list.append([summoner_name, rank.league.tier, rank.division, rank.league_points, wr, champion])

    return blue_summoners_list


def getRedTeam(match):
    red_summoners_list = []

    for item in match.red_team.participants:
        summoner_name = item.summoner.name
        champion = item.champion.name
        rank = getSummonerRank(summoner_name)
        wr = str(round(rank.wins / (rank.wins + rank.losses) * 100, 2))
        red_summoners_list.append([summoner_name, rank.league.tier, rank.division, rank.league_points, wr, champion])

    return red_summoners_list


def generateMatchString(summoner_name):
    try:
        match = getCurrentMatch(summoner_name)
        blue_summoners_list = getBlueTeam(match)
        red_summoners_list = getRedTeam(match)
        send_list = []
        for i in range(5):
            send_list.append([blue_summoners_list[i][0], f'{blue_summoners_list[i][5]}', f'{blue_summoners_list[i][1]} {blue_summoners_list[i][2]}', f'{blue_summoners_list[i][4]}%',
                              "x", f'{red_summoners_list[i][4]}%', f'{red_summoners_list[i][1]} {red_summoners_list[i][2]}', f'{red_summoners_list[i][5]}', red_summoners_list[i][0]])
        output = t2a(
            header=["Blue Side", "Champion", "Rank", "WR", "x", "WR", "Rank", "Champion", "Red Side"],
            body=send_list,
            style=PresetStyle.thin_compact
        )
    except Exception as err:
        err_string = "Esse bro não me parece tar a jogar :glean:"
        return err_string

    out_string = f"```\n{output}\n```"
    return out_string


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
        if summoner_rank != "Unranked":
            wr = str(round(summoner_rank.wins/(summoner_rank.wins+summoner_rank.losses)*100, 2))
            played = summoner_rank.wins+summoner_rank.losses
            embed = discord.Embed(title=f'{summoner.name} - Nível {summoner.level}',
                                  description=f'**{summoner_rank.league.tier} {summoner_rank.division} '
                                              f'({summoner_rank.league_points} LP) - {wr}% WR ({played} Jogos)**\n\n'
                                              f'**[OPGG](https://euw.op.gg/summoners/euw/'
                                              f'{summoner_name.replace(" ", "")})**',
                                  colour=discord.Colour.blue())
            return embed
        else:
            embed = discord.Embed(title=f'{summoner.name} - Nível {summoner.level}',
                                  description=f'**Unranked**\n\n'
                                              f'**[OPGG](https://euw.op.gg/summoners/euw/'
                                              f'{summoner_name.replace(" ", "")})**',
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
        unranked = "Unranked"
        return unranked


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
