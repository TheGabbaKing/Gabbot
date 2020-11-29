import discord
from discord.ext import commands
import random
import datetime 
import asyncio

class OmnicordGiveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----") 

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.channel.id == 780689148461449216 and message.author.id != 775935707687944192: #or message.channel.id == 775956845516029973:
            await message.add_reaction('<:yeogey:761263155292536832>')
            await message.add_reaction('<:angeleblush:778379425119993856>')
            await message.add_reaction('<:slep:693209192885911642>')
            await message.add_reaction('<:stanky:674791983272951849>')
            await message.add_reaction('<a:yuriSHOUT:740500552248459306>')

            showrole = discord.utils.get(message.guild.roles, name="Show and Tell")
            await message.author.remove_roles(showrole)

    @commands.command(name="o-giveaway")
    @commands.has_permissions(manage_guild=True)
    async def omnicord_giveaway(self, ctx, mins:int):
        embed = discord.Embed(title="Omnicord Show and Tell Giveaway", description="Enter to win the next Show and Tell")

        message = await ctx.send(embed=embed)
        await message.add_reaction("🎉")

        await asyncio.sleep(mins)

        new_msg = await ctx.channel.fetch_message(message.id)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        winner = random.choice(users)

        await ctx.send(f"Congrats {winner.mention}, you've won Show and Tell.\nPlease post your SFW video in the <#780689148461449216> channel.")
        showrole = discord.utils.get(message.guild.roles, name="Show and Tell")
        await winner.add_roles(showrole)
        
    @commands.command(name="choose-owinner")
    @commands.has_permissions(manage_guild=True)
    async def choose_omnicord_winner(self, ctx):
        await ctx.send(f"This is the current message ID: nothing")
        showandtell = self.bot.get_channel(780689148461449216)
        logs = self.bot.logs_from(showandtell, limit=1)
        await ctx.send(f"This is the current message ID: ")



def setup(bot):
    bot.add_cog(OmnicordGiveaway(bot))