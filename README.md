# A.T.S.P.-Red-Cogs
Plugins for the [Discord bot Red](https://github.com/Twentysix26/Red-DiscordBot)  
These cogs are either self-coded or modified from others. I'll definitely link to source.  
These cogs are being used on the [A.T.S.P](https://yamahi.eu) [Discord Server](http://s.yamahi.eu/chat) for several different tasks.

Install repo  
`[p]cog repo add atsp https://github.com/Nama/A.T.S.P.-Red-Cogs`  

## ToDo
**No, these are not things which I have to do. It's a cog!**  

Every user has his own ToDo list, on which they can add and remove single entries.  
Install cog  
`[p]cog install atsp todo`
* Commands *Use with your prefix*
  * help todo
  * todo  
    *Shows your own ToDo list*
  * todo add  
    *Add a new ToDo - limited to 200 characters*
* todo insert  
    *Insert a new ToDo to a position*
* todo rm Index-Number  
    *Remove a ToDo*

## Messages
Greet new members and use a broadcast with a delay on a channel  
Allows only Administrators to use the commands.  
Install cog  
`[p]cog install atsp messages`

### Commands
* welcome
  * chan  
    *Set the channel on which to greet the new members*
  * text  
    *Define the welcome message. To mention the member, put in the text `member.mention`*
* msgs
  * add  
    *Add a message to the broadcast*
  * chan  
    *Set the channel for the broadcast*
  * delay  
    *The delay in __seconds__ between the messages*
  * list  
    *Show the delay, channel and all added messages*
  * rm  
    *Remove a message from the broadcast*
  * start  
    *Start the broadcast. Channel, delay and at least one message need to be set.*
  * stop  
    *Stop the broadcast. Happens also if you add or remove messages from the broadcast.*

## Reminder
**"Forked" from [RemindMe](https://github.com/Twentysix26/Red-Cogs/)**  
Reminds you, or someone else after a specific time amount in a channel.  
Install cog  
`[p]cog install atsp reminder`

### Commands
* forgetme  
  *Removes all your active reminders*
* remind  
  *Either reminds you "me" or reminds another user. You can use their actual nick, the loginname with and without the #Numbers or just @Mention.*
* remindset  
  *Owner only - Sets a channel to remind you in.*

## RSS
**"Forked" from [RSS](https://github.com/tekulvw/Squid-Plugins)**  
Posts new feed entries in the desired channels. The fork includes filtering for keywords in the title.    
Install cog  
`[p]cog install atsp rss`

### Commands
* add  
* filter
* filter_reset  
* force
* list
* remove
* template  

## Whitelist
**"Forked" from [Mod](https://github.com/Cog-Creators/Red-DiscordBot/blob/develop/cogs/mod.py#L1131)**
Allows only the messages containing all of the set keywords. The opposite of the filter command. Keywords are set per channel instead globaly for a whole server. Deleted messages are posted to a specified channel instead of the log.
Install cog
`[p]cog install atsp whitelist`

### Commands
* add  
  *Adds words to the filter*
* remove  
  *Remove words from the filter*
* set  
  *Set a channel for the log of deleted messages*
