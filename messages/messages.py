import os
import pickle
import discord
from asyncio import sleep
from cogs.utils import checks
from discord.ext import commands


class Messages:
    '''Welcome message and periodic messages'''

    def __init__(self, bot):
        self.bot = bot
        self.bc = False
        self.config_file = 'data/messages/messages.cfg'
        self.config = pickle.load(open(self.config_file, 'rb'))

    # Welcome-Code
    @commands.group(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def welcome(self, cmd):
        '''Set a channel and a message for new members'''
        if cmd.invoked_subcommand is None:
            await self.bot.send_cmd_help(cmd)

    @welcome.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def wchan(self, cmd, text):
        '''Set the channel for the welcome message'''
        self.config['welcome'][0] = text
        pickle.dump(self.config, open(self.config_file, 'wb'))
        await self.bot.say('The channel #{0} for Welcome is saved!'.format(text))

    @welcome.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def text(self, cmd, text):
        '''Set the welcome message - put member.mention to mention the user'''
        self.config['welcome'][1] = text
        pickle.dump(self.config, open(self.config_file, 'wb'))
        await self.bot.say('Welcome message saved!')

    async def member_join(self, member):
        if self.config['welcome'][0] and self.config['welcome'][1]:
            channels = member.server.channels
            chantext = self.config['welcome'][0]
            for chan in channels:
                if chantext == chan.name:
                    channel = chan
                    break
            await self.bot.send_message(channel, self.config['welcome'][1].replace('member.mention', member.mention))

    # Broadcast-Code
    @commands.group(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def msgs(self, cmd):
        '''Manage periodic messages (broadcast)'''
        if cmd.invoked_subcommand is None:
            await self.bot.send_cmd_help(cmd)

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def stop(self, cmd):
        '''Stop the broadcast'''
        self.bc = False

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def start(self, cmd):
        '''Start the broadcast'''
        channels = cmd.message.server.channels
        chantext = self.config['chan']
        channel = False
        if not self.bc:
            if len(self.config['bc']) > 0:
                for chan in channels:
                    if chantext == chan.name:
                        channel = chan
                        break
                if channel:
                    if self.config['delay']:
                        self.bc = True
                        while self.bc:
                            for msg in self.config['bc']:
                                if self.bc:
                                    await self.bot.send_message(channel, msg)
                                    for sec in range(self.config['delay']):
                                        await sleep(1)
                                        if not self.bc:
                                            break
                                else:
                                    break
                        await self.bot.say('Broadcast stopped!')
                    else:
                        await self.bot.say('You didn\'t set a delay!')
                else:
                    await self.bot.say('You didn\'t set any channel')
            else:
                await self.bot.say('You have no messages set...')
        else:
            await self.bot.say('Broadcast is already running!')

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def list(self, cmd):
        '''List the Messages'''
        index = 0
        if len(self.config['bc']) != 0:
            msg = '**Broadcast Messages**\n*Delay*: {0}\n*Channel*: #{1}\n'.format(self.config['delay'], self.config['chan'])
            for i in self.config['bc']:
                msg += '*{0}*: {1}\n'.format(index, i)
                index += 1
            await self.bot.say(msg)
        else:
            await self.bot.say('You didn\'t set any messages...')

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def bchan(self, cmd, text):
        '''Set the channel for the broadcast'''
        self.config['chan'] = text
        pickle.dump(self.config, open(self.config_file, 'wb'))
        await self.bot.say('The channel for Broadcast is saved {0}!'.format(text))

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def delay(self, cmd, seconds):
        '''Set the delay in seconds'''
        try:
            self.config['delay'] = int(seconds)
            fine = True
        except ValueError:
            fine = False
        if fine:
            pickle.dump(self.config, open(self.config_file, 'wb'))
            await self.bot.say('Broadcast delay set to {0}!'.format(seconds))
        else:
            await self.bot.say('I need a number...')

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def add(self, cmd, text):
        '''Add a message - using quotes'''
        if self.bc:
            self.bc = False
        self.config['bc'].append(text)
        pickle.dump(self.config, open(self.config_file, 'wb'))
        await self.bot.say('New Broadcast message added!')

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def rm(self, cmd, index):
        '''Remove a message'''
        try:
            index = int(index)
            fine = True
        except ValueError:
            fine = False
        if fine:
            try:
                if self.bc:
                    self.bc = False
                self.config['bc'].pop(index)
                pickle.dump(self.config, open(self.config_file, 'wb'))
                fine = True
            except IndexError:
                fine = False
            if fine:
                await self.bot.say('Broadcast message removed!')
            else:
                await self.bot.say('The number was wrong...')
        else:
            await self.bot.say('I need a number...')


def check_data():
    path = 'data/messages'
    if not os.path.exists(path):
        print('First run setup...')
        os.makedirs(path)
    if not os.path.exists('data/messages/messages.cfg'):
        config = dict()
        config['chan'] = str()
        config['delay'] = int()
        config['bc'] = list()
        config['welcome'] = list(['', ''])
        pickle.dump(config, open('data/messages/messages.cfg', 'wb'))


def setup(bot):
    check_data()
    b = Messages(bot)
    bot.add_listener(b.member_join, 'on_member_join')
    bot.add_cog(b)
