import os
import discord
from asyncio import sleep
from cogs.utils import checks
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import pagify


class Messages:
    '''Welcome message and periodic messages'''

    def __init__(self, bot):
        self.bot = bot
        self.bc = False
        self.config_file = 'data/messages/messages.json'
        self.config = dataIO.load_json(self.config_file)

    # Welcome-Code
    @commands.group(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def welcome(self, cmd):
        '''Set a channel and a message for new members'''
        if cmd.invoked_subcommand is None:
            await self.bot.send_cmd_help(cmd)

    @welcome.command(name='chan', pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def wchan(self, cmd, channel: discord.Channel):
        '''Set the channel for the welcome message'''
        self.config['welcome'][0] = channel.id
        dataIO.save_json(self.config_file, self.config)
        await self.bot.say('The channel #{0} for Welcome is saved!'.format(channel.name))

    @welcome.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def text(self, cmd, *, text: str):
        '''Set the welcome message - put member.mention to mention the user'''
        self.config['welcome'][1] = text
        dataIO.save_json(self.config_file, self.config)
        await self.bot.say('Welcome message saved!')

    async def member_join(self, member):
        if self.config['welcome'][0] and self.config['welcome'][1]:
            channel = member.server.get_channel(self.config['welcome'][0])
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
        channel = cmd.message.server.get_channel(self.config['chan'])
        if not self.bc:
            if len(self.config['bc']) > 0:
                if channel:
                    if self.config['delay']:
                        self.bc = True
                        while self.bc:
                            for msg in self.config['bc']:
                                if self.bc:
                                    await self.bot.send_message(channel, ':loudspeaker: ' + msg)
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
            msg = ''
            for i in self.config['bc']:
                msg += '*{0}*: {1}\n'.format(index, i)
                index += 1
            for page in pagify(msg):
                user = cmd.message.author.nick or cmd.message.author.name
                embed = discord.Embed(description=msg)
                embed.title = 'Broadcast Messages'
                embed.colour = discord.Colour.blue()
                embed.set_footer(text='Channel: #{1} - Delay: {0} seconds'.format(self.config['delay'], self.config['chan']), icon_url='https://yamahi.eu/favicon.ico')
                await self.bot.say(embed=embed)
        else:
            await self.bot.say('You didn\'t set any messages...')

    @msgs.command(name='chan', pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def bchan(self, cmd, channel: discord.Channel):
        '''Set the channel for the broadcast'''
        self.config['chan'] = channel.id
        dataIO.save_json(self.config_file, self.config)
        await self.bot.say('The channel #{0} for Broadcast is saved!'.format(channel.name))

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def delay(self, cmd, seconds: int):
        '''Set the delay in seconds'''
        dataIO.save_json(self.config_file, self.config)
        await self.bot.say('Broadcast delay set to {0}!'.format(seconds))

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def add(self, cmd, *, text: str):
        '''Add a message'''
        if self.bc:
            self.bc = False
        self.config['bc'].append(text)
        dataIO.save_json(self.config_file, self.config)
        await self.bot.say('New Broadcast message added!')

    @msgs.command(pass_context=True)
    @checks.admin_or_permissions(administrator=True)
    async def rm(self, cmd, index: int):
        '''Remove a message'''
        try:
            if self.bc:
                self.bc = False
            self.config['bc'].pop(index)
            fine = True
        except IndexError:
            fine = False
        if fine:
            dataIO.save_json(self.config_file, self.config)
            await self.bot.say('Broadcast message removed!')
        else:
            await self.bot.say('The number was wrong...')


def check_data():
    path = 'data/messages'
    if not os.path.exists(path):
        print('First run setup...')
        os.makedirs(path)
    if not os.path.exists('data/messages/messages.json'):
        config = dict()
        config['chan'] = str()
        config['delay'] = int()
        config['bc'] = list()
        config['welcome'] = list(['', ''])
        dataIO.save_json('data/messages/messages.json', config)


def setup(bot):
    check_data()
    b = Messages(bot)
    bot.add_listener(b.member_join, 'on_member_join')
    bot.add_cog(b)
