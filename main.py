import discord
import os
import requests

RIOT_TOKEN = os.environ.get('RIOT_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('?summoner'):
      await message.channel.send(embed=summoner(message.content[10:]))

def summoner(summ):
  #api requests for basic shit
  summoner = requests.get('https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}'.format(summ, RIOT_TOKEN)).json()
  summonerIcon = 'https://ddragon.leagueoflegends.com/cdn/10.18.1/img/profileicon/{}.png'.format(summoner['profileIconId'])
  summMatches = requests.get('https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?api_key={}'.format(summoner['accountId'], RIOT_TOKEN)).json()
  summId = summoner['accountId']

  #grabbing most recent 10 matches
  matchIds = []
  for match in summMatches['matches']:
    matchIds.append(match['gameId'])

  #looking through most recent 10 matches and logging
  matchStats = []
  for x in range(0, 10):
    participantId = 5
    currMatch = requests.get('https://na1.api.riotgames.com/lol/match/v4/matches/{}?api_key={}'.format(matchIds[x], RIOT_TOKEN)).json()
    for participant in currMatch['participantIdentities']:
      if participant['player']['accountId'] == summId:
        participantId = participant['participantId']-1
        print(participantId)
        break
    
    kda = '{}/{}/{}'.format(currMatch['participants'][participantId]['stats']['kills'], currMatch['participants'][participantId]['stats']['deaths'], currMatch['participants'][participantId]['stats']['assists'])
    ratio = ((currMatch['participants'][participantId]['stats']['kills'] + currMatch['participants'][participantId]['stats']['assists']) / currMatch['participants'][participantId]['stats']['deaths'])
    #matchStats.append('{} - {} - {} - {} - {}'.format(currMatch['gameMode'], currMatch['participants'][participantId]['stats']['win'], currMatch[participantId]['championId'], kda, ratio))
    matchStats.append('{} / {} / {}'.format(currMatch['gameMode'], kda, ratio))
  print(matchStats)


  #begin embedding
  embedVar = discord.Embed(title=summoner['name'], description="Level: {} ID: {}".format(summoner['summonerLevel'], summId), color = 0xf47ff)
  embedVar.set_thumbnail(url = summonerIcon)

  return embedVar

client.run(os.environ.get('DISCORD_TOKEN'))