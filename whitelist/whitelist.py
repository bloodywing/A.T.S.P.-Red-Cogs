import os
import discord
from cogs.utils import checks
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from __main__ import settings
from cogs.utils.chat_formatting import pagify


class WhiteList:
    '''Allow only whitelisted words in a channel'''

    def __init__(self, bot):
        self.bot = bot
        self.filter = dataIO.load_json('data/whitelist/whitelist.json')

    @commands.group(name="wl", pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def _filter(self, ctx):
        """Adds/removes words for this channel

        Use double quotes to add/remove sentences
        Using this command with no subcommands will send
        the list of the server's filtered words."""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)
            server = ctx.message.server
            channel = ctx.message.channel
            if server.id in self.filter:
                if self.filter[server.id]:
                    words = ''
                    for chanid in self.filter[server.id].keys():
                        chan = server.get_channel(chanid)
                        newwords = "\n".join(self.filter[server.id][chanid])
                        if chan and newwords:
                            words += "Whitelisted in **#{}**:\n{}\n".format(chan, newwords)
                    for page in pagify(words, delims=[" ", "\n"], shorten_by=8):
                        if page:
                            await self.bot.say(page)

    @_filter.command(name="add", pass_context=True)
    async def filter_add(self, ctx, *words: str):
        """Adds words to the filter

        Use double quotes to add sentences
        Examples:
        filter add word1 word2 word3
        filter add \"This is a sentence\""""
        if words == ():
            await self.bot.send_cmd_help(ctx)
            return
        server = ctx.message.server
        channel = ctx.message.channel
        added = 0
        if server.id not in self.filter.keys():
            self.filter[server.id] = {}
        if channel.id not in self.filter[server.id].keys():
            self.filter[server.id][channel.id] = []
        for w in words:
            if w.lower() not in self.filter[server.id][channel.id] and w != "":
                self.filter[server.id][channel.id].append(w.lower())
                added += 1
        if added:
            dataIO.save_json('data/whitelist/whitelist.json', self.filter)
            await self.bot.say("Words added to filter.")
        else:
            await self.bot.say("Words already in the filter.")

    @_filter.command(name="remove", pass_context=True)
    async def filter_remove(self, ctx, *words: str):
        """Remove words from the filter

        Use double quotes to remove sentences
        Examples:
        filter remove word1 word2 word3
        filter remove \"This is a sentence\""""
        if words == ():
            await self.bot.send_cmd_help(ctx)
            return
        server = ctx.message.server
        channel = ctx.message.channel
        removed = 0
        if server.id not in self.filter.keys():
            await self.bot.say("There are no filtered words in this server.")
            return
        if channel.id not in self.filter[server.id].keys():
            await self.bot.say("There are no filtered words in this channel.")
            return
        for w in words:
            if w.lower() in self.filter[server.id][channel.id]:
                self.filter[server.id][channel.id].remove(w.lower())
                removed += 1
        if removed:
            dataIO.save_json('data/whitelist/whitelist.json', self.filter)
            await self.bot.say("Words removed from filter.")
        else:
            await self.bot.say("Those words weren't in the filter.")

    @checks.is_owner()
    @_filter.command(name="set", pass_context=True)
    async def filter_channel(self, ctx, channel: discord.Channel):
        """Set a channel for the log of deleted messages"""
        server = ctx.message.server
        self.filter[server.id]["channel"] = channel.id
        dataIO.save_json('data/whitelist/whitelist.json', self.filter)
        await self.bot.say("Channel set!")

    async def on_message(self, message):
        author = message.author
        if message.server is not None or self.bot.user != author:
            valid_user = isinstance(author, discord.Member) and not author.bot
            if valid_user and not self.is_mod_or_superior(message):
                await self.check_whitelist(message)

    async def on_message_edit(self, _, message):
        author = message.author
        if message.server is not None or self.bot.user != author:
            valid_user = isinstance(author, discord.Member) and not author.bot
            if valid_user and not self.is_mod_or_superior(message):
                await self.check_whitelist(message)

    async def check_whitelist(self, message):
        server = message.server
        channel = message.channel
        if channel.id in self.filter[server.id].keys():
            for w in self.filter[server.id][channel.id]:
                if w not in message.content.lower():
                    log_channel = server.get_channel(self.filter[server.id]["channel"])
                    try:
                        await self.bot.delete_message(message)
                        await self.bot.send_message(log_channel,
                                                    "Message from **{}** deleted in **#{}**. Message:\n{}".format(
                                                        message.author, server.get_channel(channel.id),
                                                        message.content))
                        return True
                    except:
                        await self.bot.send_message(log_channel,
                                                    "Something went wrong while deleting a message from **{}** in **#{}**. Message:\n{}".format(
                                                        message.author, server.get_channel(channel.id),
                                                        message.content))

        return False

    def is_mod_or_superior(self, obj):
        if isinstance(obj, discord.Message):
            user = obj.author
        elif isinstance(obj, discord.Member):
            user = obj
        elif isinstance(obj, discord.Role):
            pass
        else:
            raise TypeError('Only messages, members or roles may be passed')

        server = obj.server
        admin_role = settings.get_server_admin(server)
        mod_role = settings.get_server_mod(server)

        if isinstance(obj, discord.Role):
            return obj.name in [admin_role, mod_role]

        if user.id == settings.owner:
            return True
        elif discord.utils.get(user.roles, name=admin_role):
            return True
        elif discord.utils.get(user.roles, name=mod_role):
            return True
        else:
            return False


def check_data():
    path = 'data/whitelist'
    if not os.path.exists(path):
        print('First run setup...')
        os.makedirs(path)
    if not os.path.exists(os.path.join(path, 'whitelist.json')):
        dataIO.save_json(os.path.join(path, 'whitelist.json'), {})


def setup(bot):
    check_data()
    bot.add_cog(WhiteList(bot))
