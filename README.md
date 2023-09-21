# Just another CTF Discord bot

Quick and dirty discord bot made for our CTF Team. Largely inspired by other similar bots, created due to how awkward some where to use.
Basic features include:
- Create a CTF Role that players can add or remove themselves from, to notify all interested players when a CTF is starting
- Create, delete, and archive a CTF channel
- Create and delete challenge threads inside each CTF channel, and mark them as solved/unsolved
- List all current challenges in that particular CTF

## Usage
On joinning a server, it creates a "CTF Player" role and:
- "CTF Chat" category
  - register-here channel - contains an embed with buttons to add/remove yourself from the CTF Player role at any time
  - bot-chat channel - CTFs can only be created from this place, to keep spam contained
- "Running CTFs" category - will contain all currently running CTFs
- "Archives" category - Will contain all archived CTFs, this is set as read-only

## Commands:
```
Call the bot with: $ctf
$ctf create [ctf name] - Creates a new ctf
$ctf help - Displays the help message

Only callable from within a CTF channel
$ctf creds [user] [password] - Sends and pins a message containing the set user:password credentials for the team, for that particular CTF. Re-running the same command overwrites the set credentials
$ctf add [chall name] - Creates a new challenge thread, unsolved by default
$ctf ls - Lists all challenges for that CTF
$ctf rmctf - Deletes the CTF
$ctf archive - Moves the CTF channel to the archive category, making it Read-Only

Only callable from within a Challenge thread
$ctf rm - Deletes the current challenge thread
$ctf solve - Sets the challenge as solved
$ctf unsolve - Sets the challenge as unsolved
```

Will probably contain bugs, errors, and issues.
No guarantees that it won't mess up your server, only being tested in a trusted environment (as in, we can trust our users)
