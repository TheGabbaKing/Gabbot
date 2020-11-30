import discord
from discord.ext import commands
import platform
import os
import os.path, time
import asyncio
import traceback
import datetime

import cogs._json

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")  
              
    # STATISTICS command
    @commands.command()
    async def statistics(self, ctx):

        """
        Displays information about the bot statistics
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members())) 

        embed = discord.Embed(title=f'Gabbot:registered::tm: Stats',colour=0xd54549, timestamp=ctx.message.created_at)

        embed.add_field(name='Total Servers:', value=serverCount, inline = True)
        embed.add_field(name='Total Users:', value=memberCount, inline = True)
        embed.add_field(name="\uFEFF", value="\uFEFF", inline = True)
        embed.add_field(name='Bot Version:', value=self.bot.version, inline = True)
        embed.add_field(name='Bot Developer:', value="<@487110546223661076>", inline = True)
        embed.add_field(name="\uFEFF", value="\uFEFF", inline = True)

        embed.set_footer(text=f"{self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    # LOGOUT command
    @commands.command(aliases=['disconnect', 'goodbye', 'close', 'stopbot', 'fuckoff'])
    @commands.is_owner()
    async def logout(self, ctx):
        """
        If the user running the command owns the bot then this will disconnect the bot from discord.
        """
        
        await ctx.send(f"Later, loser.")
        await ctx.send(f"<a:jiwonsalute:780716129349009438>")
        await self.bot.logout()

    # ECHO command
    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx, *, message=None):
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "Please provide a message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)
        # await echoMsg.add_reaction('<:yeogey:761263155292536832>')

    @commands.command(
        name='reload', description="Reload all/one of the bots cogs!"
    )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)

    # BLACKLIST command
    @commands.command()
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("You can't blacklist yourself, idiot.")
            return
        self.bot.blacklisted_users.append(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"{user.name} has been blacklisted.")

    # UNBLACKLIST command
    @commands.command()
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        self.bot.blacklisted_users.remove(user.id)
        data = cogs._json.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._json.write_json(data, "blacklist")
        await ctx.send(f"{user.name} has been unblacklisted.")

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 20, commands.BucketType.default)
    async def prefix(self, ctx, *, pre='g.'):
        """
        Set a custom prefix for a server
        """
        data = cogs._json.read_json('prefixes')
        data[str(ctx.message.guild.id)] = pre
        cogs._json.write_json(data, 'prefixes')
        await ctx.send(f"Your server may now summon **Gabbot**:registered::tm: using the prefix `{pre}`")

    @commands.command()
    async def it(self, ctx):
        """
        Sends a link to the Gabbot github repository
        """
        await ctx.send('The Gabbot:registered::tm: github can be found here:\n https://github.com/TheGabbaKing/Gabbot')

    @commands.command()
    @commands.is_owner()
    async def updated(self, ctx):
        commandsUpdated = os.path.getmtime(".\cogs\commands.py")
        eventsUpdated = os.path.getmtime(".\cogs\events.py")
        commandsModTime = datetime.datetime.fromtimestamp(commandsUpdated).strftime("%c")
        eventsModTime = datetime.datetime.fromtimestamp(eventsUpdated).strftime("%c")

        await ctx.send(f"`Commands Last Modified:` {commandsModTime}")
        await ctx.send(f"`Events Last Modified:` {eventsModTime}")


# Sets up bot
def setup(bot):
    bot.add_cog(Commands(bot))