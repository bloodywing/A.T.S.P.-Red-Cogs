import os
import discord
from cogs.utils import checks
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import pagify


class ToDo:
    '''Manage your ToDo list'''

    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'data/todo/todo.json'
        self.config = dataIO.load_json(self.config_file)

    @commands.group(pass_context=True)
    async def todo(self, cmd):
        '''Make your own ToDo list and manage it'''
        if cmd.invoked_subcommand is None:
            try:
                user = str(cmd.message.author)
                index = 0
                if len(self.config[user]) != 0:
                    msg = ''
                    for i in self.config[user]:
                        msg += '*{0}*: {1}\n'.format(index, i)
                        index += 1
                    page_index = 1
                    pages = pagify(msg)
                    for page in pages:
                        nick = cmd.message.author.nick or cmd.message.author.name
                        embed = discord.Embed(description=page)
                        embed.title = '{}\'s ToDo of {} things'.format(nick, len(self.config[user]))
                        embed.colour = discord.Colour.green()
                        embed.set_footer(text='Part {}'.format(page_index), icon_url='https://yamahi.eu/favicon.ico')
                        await self.bot.say(embed=embed)
                        page_index += 1
                else:
                    await self.bot.say('You have nothing to do! :D')
            except KeyError:
                await self.bot.say('You have nothing to do! :D')
            except:
                await self.bot.say('An error happened?!')

    @todo.command(pass_context=True)
    async def add(self, cmd, *, text: str):
        '''Add something to do'''
        user = str(cmd.message.author)
        if user not in self.config:
            self.config[user] = list()
        if len(text) <= 200:
            self.config[user].append(text)
            dataIO.save_json(self.config_file, self.config)
            await self.bot.say('New ToDo added!')
        else:
            await self.bot.say('Max. 200 characters allowed!')

    @todo.command(pass_context=True)
    async def insert(self, cmd, index: int, *, text: str):
        '''Add something to do'''
        user = str(cmd.message.author)
        if user not in self.config:
            self.config[user] = list()
        if len(text) <= 200:
            self.config[user].insert(index, text)
            dataIO.save_json(self.config_file, self.config)
            await self.bot.say('New ToDo added!')
        else:
            await self.bot.say('Max. 200 characters allowed!')

    @todo.command(pass_context=True)
    async def rm(self, cmd, index: int):
        '''Remove something you did already'''
        user = str(cmd.message.author)
        if user in self.config:
            try:
                self.config[user].pop(index)
                dataIO.save_json(self.config_file, self.config)
                fine = True
            except IndexError:
                fine = False
            if fine:
                await self.bot.say('ToDo removed!')
            else:
                await self.bot.say('The number was wrong...')
        else:
            await self.bot.say('You have nothing to do! :D')


def check_data():
    path = 'data/todo'
    if not os.path.exists(path):
        print('First run setup...')
        os.makedirs(path)
    if not os.path.exists('data/todo/todo.json'):
        dataIO.save_json('data/todo/todo.json', [])


def setup(bot):
    check_data()
    bot.add_cog(ToDo(bot))
