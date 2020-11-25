import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")  

    @commands.command()
    async def addrole(ctx, role: discord.Role, user: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            await user.add_roles(role)
            await ctx.send(f"Successfully applied")

    @commands.command()
    async def remove(ctx, role: discord.Role, user: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            await user.remove_roles(role)
            await ctx.send(f"Successfully removed")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick (self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(user=member, reason=reason)

        channel = self.bot.get_channel(776973473519108096)
        embed = discord.Embed(title=f"{ctx.author.name} kicked: {member.name}", description=reason)
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason)

        channel = self.bot.get_channel(776973473519108096)
        embed = discord.Embed(title=f"{ctx.author.name} banned: {member.name}", description=reason)
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member, *, reason=None):
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member, reason=reason)

        channel = self.bot.get_channel(776973473519108096)
        embed = discord.Embed(title=f"{ctx.author.name} unbanned: {member.name}", description=reason)
        await channel.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=15):
        await ctx.channel.purge(limit=amount+1)

        channel = self.bot.get_channel(776973473519108096)
        embed = discord.Embed(title=f"{ctx.author.name} deleted {amount} messages in {ctx.channel.name}")
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))