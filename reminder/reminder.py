import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from cogs.utils import checks
import os
import re
import asyncio
import time
import logging
import datetime
from dateutil.relativedelta import relativedelta

class Reminder:
    """Never forget anything anymore."""

    def __init__(self, bot):
        self.bot = bot
        self.reminders = fileIO("data/reminder/reminders.json", "load")
        
    @commands.command(pass_context=True)
    async def remind(self, ctx, user: str, time_unit: str, *, text: str):
        """Sends you <text> when the time is up

        Accepts: minutes, hours, days, weeks, month
        Example:
        [p]remind me 3 days Have sushi with Asu and JennJenn
        [p]remind Asu 2 months Buy JennJenn a Coke"""
        if not self.reminders[0]["CHANNEL"]:
            await self.bot.say("Set a channel first `remindset #channel`!")
            return
        author = ""
        notme = ctx.message.server.get_member_named(user)
        if user == 'me':  # There might be a problem if a user exists with that name
            author = ctx.message.author
        elif notme:
            author = notme
        else:
            author = ctx.message.server.get_member(user[2:-1].replace("!", ""))
        if not author:
            await self.bot.say("The user {0} doesn't exist!".format(user))
            return
        s = ""
        
        future_matches = re.findall(r'\d{1,2}\w', time_unit)
        unit_convert_dict = {
            's': 'seconds',
            'm': 'minutes',
            'h': 'hours',
            'M': 'months',
            'w': 'weeks',
            'd': 'days',
            'y': 'years'
        }
        
        delta = relativedelta()
        for m in future_matches:
           _, unit = re.split('\d+', m)    
           delta_unit = unit_convert_dict.get(unit, 'minutes')
           delta += relativedelta(**{delta_unit: int(re.match('\d+', m).group())}) 
        future = (datetime.datetime.now() + delta).timestamp()
        
        self.reminders.append({"ID": author.id, "FUTURE": future, "TEXT": text})
        logger.info("{} ({}) set a reminder.".format(author.name, author.id))
        await self.bot.say("I will remind {} that in {}.".format(author.name, time_unit))
        fileIO("data/reminder/reminders.json", "save", self.reminders)

    @checks.is_owner()
    @commands.command(pass_context=True)
    async def remindset(self, ctx, channel: discord.Channel):
        """Set a channel in which to remind the users"""
        self.reminders[0]["SERVER"] = ctx.message.server.id
        self.reminders[0]["CHANNEL"] = channel.id
        fileIO("data/reminder/reminders.json", "save", self.reminders)
        await self.bot.say("Channel set!")

    @commands.command(pass_context=True)
    async def forgetme(self, ctx):
        """Removes all your upcoming notifications"""
        author = ctx.message.author
        to_remove = []
        for reminder in self.reminders[1:]:
            if reminder["ID"] == author.id:
                to_remove.append(reminder)

        if not to_remove == []:
            for reminder in to_remove:
                self.reminders.remove(reminder)
            fileIO("data/reminder/reminders.json", "save", self.reminders)
            await self.bot.say("All your notifications have been removed.")
        else:
            await self.bot.say("You don't have any upcoming notification.")

    async def check_reminders(self):
        await asyncio.sleep(60)
        serverid = self.reminders[0]["SERVER"]
        for server in self.bot.servers:
            if server.id == serverid:
                channel = server.get_channel(self.reminders[0]["CHANNEL"])
                break
        while self is self.bot.get_cog("Reminder"):
            to_remove = []
            for reminder in self.reminders[1:]:
                if reminder["FUTURE"] <= int(time.time()):
                    try:
                        await self.bot.send_message(channel, discord.User(id=reminder["ID"]).mention + " remember to {}".format(reminder["TEXT"]))
                    except (discord.errors.Forbidden, discord.errors.NotFound):
                        to_remove.append(reminder)
                    except discord.errors.HTTPException:
                        pass
                    else:
                        to_remove.append(reminder)
            for reminder in to_remove:
                self.reminders.remove(reminder)
            if to_remove:
                fileIO("data/reminder/reminders.json", "save", self.reminders)
            await asyncio.sleep(5)


def check_folders():
    if not os.path.exists("data/reminder"):
        print("Creating data/reminder folder...")
        os.makedirs("data/reminder")


def check_files():
    f = "data/reminder/reminders.json"
    if not fileIO(f, "check"):
        print("Creating empty reminders.json...")
        fileIO(f, "save", [{"channel": ""}])


def setup(bot):
    global logger
    check_folders()
    check_files()
    logger = logging.getLogger("reminder")
    if logger.level == 0: # Prevents the logger from being loaded again in case of module reload
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='data/reminder/reminders.log', encoding='utf-8', mode='a')
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s', datefmt="[%d/%m/%Y %H:%M]"))
        logger.addHandler(handler)
    n = Reminder(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.check_reminders())
    bot.add_cog(n)
