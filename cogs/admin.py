import discord
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'
        .format(self.client))

    # Before Commands
    async def cog_check(self, ctx):
        return ctx.author.guild_permissions.administrator

    # Commands
    @commands.command()
    async def setbotchannel(self, ctx, message):
        channel = discord.utils.get(ctx.guild.channels, name=message)
        if channel:
            self.client.designated_channel = channel
            await ctx.channel.send(f"My new home has been set to {channel.name}")
        else:
            await ctx.channel.send(f'Could not find any channel named {message}')

    @commands.command()
    async def setemoji(self, ctx, message):
        if len(message) == 1:
            self.client.emoji = message
        else:
            await ctx.channel.send("Needs to be only one character. Note that discord does not support adding custom emoji's to nicknames")

    @commands.command()
    async def setaddword(self, ctx, message):
        self.client.adder_word = message
        await ctx.channel.send(f"New word for adding {self.client.emoji} is '{self.client.adder_word}'")

    @commands.command()
    async def setsubtractword(self, ctx, message):
        self.client.subtractor_word = message
        await ctx.channel.send(f"New word for removing all {self.client.emoji} is '{self.client.subtractor_word}'")

    @commands.command()
    async def setplagueword(self, ctx, message):
        self.client.plague_word = message
        await ctx.channel.send(f"New word for plaguing the server with {self.client.emoji} is '{self.client.plague_word}'")

    @commands.command()
    async def resetall(self, ctx):
        self.client.subtractor_word = 'that'
        self.client.adder_word = 'this'
        self.client.plague_word = 'spread'
        self.client.emoji = '🌽'
        await ctx.channel.send(f"Reset: Emoji to {self.client.emoji}, Add word to '{self.client.adder_word}', clear all word to '{self.client.subtractor_word}', and plague word to '{self.client.plague_word}'")

    @commands.command()
    async def values(self, ctx):
        await ctx.channel.send(f"Emoji is set to {self.client.emoji}, Add word is set to '{self.client.adder_word}', clear all word is set to '{self.client.subtractor_word}', and plague word is set to '{self.client.plague_word}'")

    @commands.command()
    async def removeall(self, ctx):
        members = await ctx.guild.fetch_members(limit=None).flatten()
        filtered_members = []
        for member in members:
            if member.nick != None and f'{self.client.emoji}' in member.nick:
                filtered_members.append(member)

        for member in filtered_members:
            await member.edit(nick=f"{member.nick}".replace(f"{self.client.emoji}",""))

        await ctx.channel.send(f'I have wipped out the {self.client.emoji} plague.')
        await ctx.channel.send(f'Everyone has lost their {self.client.emoji}')

def setup(client):
    client.add_cog(Admin(client))
