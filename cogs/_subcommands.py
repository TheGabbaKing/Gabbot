import discord
from discord.ext import commands

class SubCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")  

    @commands.group()
    async def first(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("This is the first command layer")
    
    @first.group()
    async def second(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("This is the second command layer")
    
    @second.command()
    async def third(self, ctx):        
        await ctx.send("This is the bottom command layer")
    
def setup(bot):
    bot.add_cog(SubCommands(bot))