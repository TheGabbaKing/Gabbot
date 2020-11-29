import discord
from discord.ext import commands
import random
import datetime 
import asyncio

class KaicordGiveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----") 

    @commands.command(name="k-giveaway")
    @commands.has_permissions(manage_guild=True)
    async def kaicord_giveaway(self, ctx, mins:int):
        embed = discord.Embed(title="Kaicord Show and Tell Giveaway", description="Enter to win the next Show and Tell")

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
        
    @commands.command(name="choose-kwinner")
    @commands.has_permissions(manage_guild=True)
    async def choose_kaicord_winner(self, ctx):
        await ctx.send(f"This is the current message ID: nothing")
        showandtell = self.bot.get_channel(780689148461449216)
        logs = self.bot.logs_from(showandtell, limit=1)
        messageID = logs.messageID
        await ctx.send(f"This is the current message ID: {messageID}")



def setup(bot):
    bot.add_cog(KaicordGiveaway(bot))