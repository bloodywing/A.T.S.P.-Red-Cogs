import os
import pickle
import discord
from discord.ext import commands
from cogs.utils.dataIO import dataIO


class ToDo:
    """Manage your ToDo list"""

    def __init__(self, bot):
        self.bot = bot
        self.config_file = 'data/todo/todo.cfg'
        self.config = pickle.load(open(self.config_file, 'rb'))

    @commands.group(pass_context=True)
    async def todo(self, cmd):
        """Make your own ToDo list and manage it"""
        if cmd.invoked_subcommand is None:
            try:
                user = str(cmd.message.author)
                index = 0
                if len(self.config[user]) != 0:
                    for i in self.config[user]:
                        await self.bot.say('{0}: {1}'.format(index, i))
                        index += 1
                else:
                    await self.bot.say('Yo have nothen to do...')
            except KeyError:
                await self.bot.say('Yo have nothen to do...')
            except:
                await self.bot.say('An error happened?!')

    @todo.command(pass_context=True)
    async def add(self, cmd, text):
        '''Add something to do'''
        user = str(cmd.message.author)
        if user not in self.config:
            self.config[user] = list()
        self.config[user].append(text)
        pickle.dump(self.config, open(self.config_file, 'wb'))
        await self.bot.say('its saved m8')

    @todo.command(pass_context=True)
    async def rm(self, cmd, index):
        '''Remove something you did already - put your text in quotes'''
        user = str(cmd.message.author)
        if user in self.config:
            try:
                index = int(index)
                fine = True
            except ValueError:
                fine = False
            if fine:
                try:
                    self.config[user].pop(index)
                    pickle.dump(self.config, open(self.config_file, 'wb'))
                    fine = True
                except IndexError:
                    fine = False
                if fine:
                    await self.bot.say('ToDo updated!')
                else:
                    await self.bot.say('The number was wrong...')
            else:
                await self.bot.say('I need a number...')
        else:
            await self.bot.say('You have nothing to do! :D')


def check_data():
    path = 'data/todo'
    if not os.path.exists(path):
        print('First run setup...')
        os.makedirs(path)
    if not os.path.exists('data/todo/todo.cfg'):
        pickle.dump(dict(), open('data/todo/todo.cfg', 'wb'))


def setup(bot):
    check_data()
    bot.add_cog(ToDo(bot))
