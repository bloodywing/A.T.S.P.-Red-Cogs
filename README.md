# A.T.S.P.-Red-Cogs
Plugins for the [Discord bot Red](https://github.com/Twentysix26/Red-DiscordBot)  
These cogs are either self-coded or modified from others. I'll definitely link to source.  
These cogs are being used on the [A.T.S.P](https://yamahi.eu) [Discord Server](http://s.yamahi.eu/chat) for several different tasks.

Install repo  
`[p]cog repo add atsp https://github.com/Nama/A.T.S.P.-Red-Cogs`  

## ToDo
**No, these are not things which I have to do. It's a cog!**  

Every user has his own ToDo list, on which they can add and remove single entries.  
~~-Allows only Moderators and above to use the commands.~~  
Install cog  
`[p]cog install atsp todo`
* Commands *Use with your prefix*
  * help todo
  * todo  
    *Shows your own ToDo list*
  * todo add  
    *Add a new ToDo - limited to 200 characters*
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
    *Start the broadcast. Channel, delay and at leat one message need to be set.*
  * stop  
    *Stop the broadcast. Happens also if you add or remove messages from the broadcast.*

## Reminder
**"Forked" from [RemindMe](https://github.com/Twentysix26/Red-Cogs/)**  
Reminds you, or someone else after a specific time amount.  
Install cog  
`[p]cog install atsp reminder`

### Commands
* forgetme  
  *Removes all your active reminders*
* remind  
  *Either reminds you "me" or reminds another user. You can use their actual nick, the loginname with and without the #Numbers or just @Mention.*
