import discord
from discord.ext import commands
import os
import os.path, time

import cogs._json

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")  

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #Ignore these errors
        ignored = (commands.UserInputError)
        if isinstance(error, ignored):
            return

        theError = (f'{error}')
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f'The command {theError[8:-13]} does not exist')
            
        if isinstance(error, commands.CommandOnCooldown):
            # If the command is currently on cooldown trip this
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f' You must wait {int(s)} seconds to use this command!')
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
            else:
                await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
        elif isinstance(error, commands.CheckFailure):
            # If the command has failed a check, trip this
            await ctx.send("Ay watch it, you don't have permission to do this command.")
            raise error

    @commands.Cog.listener()
    async def on_message(self, message):
        
        # Whenever bot is tagged, respond with it's prefix
        if message.content.startswith(f"<@!{self.bot.user.id}>") and len(message.content) == len(
        f"<@!{self.bot.user.id}>"
            ):
            data = cogs._json.read_json('prefixes')
            if str(message.guild.id) in data:
                prefix = data[str(message.guild.id)]
            else:
                prefix = 'g.'
            prefixMsg = await message.channel.send(f"The **Gabbot**:registered::tm: prefix is `{prefix}`")
            await prefixMsg.add_reaction('<:yeogey:761263155292536832>')
            await prefixMsg.add_reaction('<:slep:693209192885911642>')
            await prefixMsg.add_reaction('<:stanky:674791983272951849>')
            await prefixMsg.add_reaction('<a:yuriSHOUT:740500552248459306>')

        if 'yeogey'.casefold() in message.content.casefold():
            await message.add_reaction('<:yeogey:761263155292536832>')

    

# Sets up bot
def setup(bot):
    bot.add_cog(Events(bot))