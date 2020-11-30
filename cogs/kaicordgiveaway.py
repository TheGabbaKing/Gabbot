import discord
from discord.ext import commands, tasks
import random
import datetime 
import asyncio

class KaicordGiveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.kaicord_giveaway_task.start()
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----") 

    @tasks.loop(seconds=30)
    async def kaicord_giveaway_task(self):
        
        print('Kaicord started!')

        showandtell = self.bot.get_channel(780689148461449216)

        embed = discord.Embed(title="Kaicord Show and Tell Giveaway", description="Enter to win the next Show and Tell")
        
        message = await showandtell.send(embed=embed)
        await message.add_reaction("🎉")

        await asyncio.sleep(86390)

        new_msg = await showandtell.fetch_message(message.id)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        usersName = []
        for i in users:
            usersName.append(i.name)
        await self.bot.get_channel(623997789306617856).send(f"**Reacted by: ** {', '.join(usersName)}")

        winner = random.choice(users)

        await showandtell.send(f"Congrats {winner.mention}, you've won Show and Tell.\nPlease post your SFW content in the <#780689148461449216> channel.")
        showrole = discord.utils.get(message.guild.roles, name="Show and Tell")
        await winner.add_roles(showrole)

    @kaicord_giveaway_task.before_loop
    async def before_kgiveaway(self):
        print('waiting...')
        await self.bot.wait_until_ready()

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

        await ctx.send(f"Congrats {winner.mention}, you've won Show and Tell.\nPlease post your SFW content in the <#780689148461449216> channel.")
        showrole = discord.utils.get(message.guild.roles, name="Show and Tell")
        await winner.add_roles(showrole)
        
    @commands.command(name="choose-kwinner")
    @commands.has_permissions(manage_guild=True)
    async def choose_kaicord_winner(self, ctx):
        
        showandtell = self.bot.get_channel(780689148461449216)
        await ctx.send(f"Channel fetched")

        recent = await showandtell.history(limit = 2).flatten()
        
        users = await recent[1].reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        await ctx.send(f"reactions found")

        winner = random.choice(users)
        await ctx.send(f"winner chosen")

        await showandtell.send(f"Congrats {winner.mention}, you've won Show and Tell.\nPlease post your SFW content in the <#780689148461449216> channel.")
        showrole = discord.utils.get(recent[1].guild.roles, name="Show and Tell")
        await winner.add_roles(showrole)



def setup(bot):
    bot.add_cog(KaicordGiveaway(bot))