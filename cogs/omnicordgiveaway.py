import discord
from discord.ext import commands, tasks
import random
import datetime 
from datetime import timedelta
import asyncio

class OmnicordGiveaway(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.omnicord_giveaway_task.start()
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----") 

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.channel.id == 782766078995988510 and message.author.id != 775935707687944192: #or message.channel.id == 775956845516029973:
            await message.add_reaction('<:yeogey:761263155292536832>')
            await message.add_reaction('<:flooshed:782834444846759956>')
            await message.add_reaction('<:MiyeonOOP:647029478081691661>')
            await message.add_reaction('<:somicry:782820489525461042>')
            await message.add_reaction('<:stanky:674791983272951849>')
            await message.add_reaction('<:slep:693209192885911642>')

            showrole = discord.utils.get(message.guild.roles, name="Show and Tell")
            await message.author.remove_roles(showrole)

    @tasks.loop(hours=24)
    async def omnicord_giveaway_task(self):
        
        print('Omnicord started!')

        showandtellOmni = self.bot.get_channel(782766078995988510)

        embed = discord.Embed(title="Omnicord Show and Tell Giveaway", description="Enter to win the next Show and Tell")
        embed.set_footer(text=f"Giveaway ends at 11am UTC (24 hours from this message).")
        
        message = await showandtellOmni.send(embed=embed)
        await message.add_reaction("🎉")

        await asyncio.sleep(86390)

        new_msg = await showandtellOmni.fetch_message(message.id)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))

        usersName = []
        for i in users:
            usersName.append(i.name)
        await self.bot.get_channel(656260924256288778).send(f"**Reacted by: ** {', '.join(usersName)}")

        winner = random.choice(users)

        await showandtellOmni.send(f"Congrats {winner.mention}, you've won Show and Tell.\nPlease post your SFW content in the <#780689148461449216> channel.")
        showrole = discord.utils.get(message.guild.roles, name="Show and Tell")
        await winner.add_roles(showrole)
    
    @omnicord_giveaway_task.before_loop
    async def before_ogiveaway(self):
        print('Omnicord waiting...')
        await self.bot.wait_until_ready()

        delayTime = (timedelta(hours=24) - (datetime.datetime.utcnow()- datetime.datetime.utcnow().replace(hour=11, minute=00, second=0, microsecond=0))).total_seconds() % (24 * 3600)
        await asyncio.sleep(delayTime)

    @commands.command(name="o-giveaway")
    @commands.has_permissions(manage_guild=True)
    async def omnicord_giveaway(self, ctx, mins:int):
        embed = discord.Embed(title="Omnicord Show and Tell Giveaway", description="Enter to win the next Show and Tell")
        embed.set_footer(text=f"Giveaway ends at 11am UTC (24 hours from this message).")
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
        
    @commands.command(name="choose-owinner")
    @commands.has_permissions(manage_guild=True)
    async def choose_omnicord_winner(self, ctx):
        showandtell = self.bot.get_channel(782766078995988510)
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
    bot.add_cog(OmnicordGiveaway(bot))