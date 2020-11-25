import discord
from discord.ext import commands
import logging
from pathlib import Path
import json
import os

import cogs._json

# current working directory
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"The Current Working Directory is: {cwd}\n-----")

def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('g.')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

# definitions

# MUST create a secrets.json folder yourself and add it to that folder and put the 'token' in there
secret_file = json.load(open(cwd+'/json_files/secrets.json')) 
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=487110546223661076) # Bot is the same as Client 
bot.config_token = secret_file['token'] # sets discord bot token
logging.basicConfig(level=logging.INFO) # 


bot.blacklisted_users = [] # blacklisted users list
bot.cwd = cwd

bot.version = 'alpha 0.1.4' # bot version

# bot events
@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: g.\n-----") #prints the Bot name, id and prefix
    await bot.change_presence(activity=discord.Game(name="with my pp \n| g.")) #changes the bots activity

@bot.event
async def on_message(message):
    #ignore ourselves
    #if message.author.id == bot.user.id:
    #    return
    #
    #if message.author.id in bot.blacklisted_users:
    #    return
    await bot.process_commands(message)



if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E. it's not being imported from another python file like this 
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    
    bot.run(bot.config_token)


#@logout.error # Logout error handler
#async def logout_error(ctx, error):
    #"""
    #"""
    #if isinstance(error, commands.CheckFailure):
    #    await ctx.send("Oi cunt, I'm not going anywhere. Only Gabba can tell me what to do")
    #else:
    #    raise error

    #Ignore these errors
    