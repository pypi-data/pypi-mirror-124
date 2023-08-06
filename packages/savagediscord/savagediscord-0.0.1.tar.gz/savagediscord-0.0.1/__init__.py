import discord
from discord.ext import commands

def setupBot(prefix):
    global client
    client = commands.Bot(command_prefix = prefix)


def botPlaying(activity):
    global actv
    actv = activity

def runBot(key):
    @client.event
    async def on_ready():
        print('[LOGS] Bot is ready!')
        print("""[LOGS] Logged in as: {}\n[LOGS] ID: {}""".format(client.user.name, client.user.id))
        try:
            await client.change_presence(activity=discord.Game(name=actv))
        except:
            await client.change_presence(activity=discord.Game(name='Savage Discord'))
    
    client.run(key)