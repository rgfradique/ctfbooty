import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import os

#Names you want to give to channels
register_channel_name = "register-here"
bot_channel_name = "bot-chat"
ctf_role = "CTF Player"
running_category = "Running CTFs"
ctf_category = "CTF Chat"
archive_category = "Archives"
solved_string = "✅"
unsolved_string = "❌"

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

class HelpMenu(commands.MinimalHelpCommand):
    async def send_pages(self):
        channel = self.get_destination()
        if str(channel.category) == str(running_category) or str(channel.category)==str(ctf_category):
            for page in self.paginator.pages:
                emby = discord.Embed(description=page)
                await channel.send(embed=emby)

client = commands.Bot(command_prefix="$ctf ", intents=intents, help_command = HelpMenu())

def set_archives_perms():
    perms = discord.PermissionOverwrite()
    perms.stream=False
    perms.request_to_speak=False
    perms.move_members=False
    perms.use_soundboard=False
    perms.manage_roles=False
    perms.embed_links=False
    perms.external_stickers=False
    perms.manage_messages=False
    perms.priority_speaker=False
    perms.external_emojis=False
    perms.deafen_members=False
    perms.attach_files=False
    perms.send_tts_messages=False
    perms.use_application_commands=False
    perms.create_private_threads=False
    perms.manage_events=False
    perms.speak=False
    perms.create_instant_invite=False
    perms.send_messages=False
    perms.send_voice_messages=False
    perms.mention_everyone=False
    perms.connect=False
    perms.use_voice_activation=False
    perms.manage_webhooks=False
    perms.mute_members=False
    perms.use_embedded_activities=False
    perms.send_messages_in_threads=False
    perms.manage_threads=False
    perms.use_external_sounds=False
    perms.create_public_threads=False
    perms.add_reactions=False
    perms.manage_channels=False
    return perms

def set_everyone_perms():
    perms = discord.PermissionOverwrite()
    perms.send_messages_in_threads=True
    perms.use_voice_activation=False
    perms.attach_files=True
    perms.manage_threads=False
    perms.read_message_history=True
    perms.speak=False
    perms.mention_everyone=False
    perms.manage_channels=False
    perms.manage_messages=False
    perms.external_emojis=True
    perms.use_soundboard=False
    perms.create_instant_invite=True
    perms.manage_roles=False
    perms.priority_speaker=False
    perms.manage_webhooks=False
    perms.stream=False
    perms.request_to_speak=False
    perms.read_messages=True
    perms.move_members=False
    perms.send_tts_messages=False
    perms.mute_members=False
    perms.send_voice_messages=False
    perms.embed_links=True
    perms.add_reactions=True
    perms.create_public_threads=False
    perms.create_private_threads=False
    perms.connect=False
    perms.use_embedded_activities=False
    perms.send_messages=True
    perms.manage_events=False
    perms.use_application_commands=False
    perms.external_stickers=True
    perms.deafen_members=False
    perms.use_external_sounds=False
    return perms

def strip_status(chall_name):
    return chall_name.replace(solved_string,'').replace(unsolved_string,'')

def parse_ch_names(name):
    return name.lower().replace(" ","-")

def get_names(obj_list):
    nl = []
    for i in obj_list:
        nl.append(i.name)
    return nl

def get_cat_chan(message):
    chan = message.channel
    cat = chan.category
    return cat, chan

async def create_role(guild_obj, role_name):
    ctf_pr = discord.utils.get(guild_obj.roles, name=role_name)
    if ctf_pr == None:
        ctf_pr = await guild_obj.create_role(name=role_name,color=discord.Color.dark_gold())
    return ctf_pr

class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="CTF me!", style=discord.ButtonStyle.green, emoji="✅", custom_id="add")
    async def add_callback(self, interaction,button):
        role_user = interaction.user
        ctfr = discord.utils.get(interaction.guild.roles, name=ctf_role)
        if ctfr != None:
            await role_user.add_roles(ctfr)
            await interaction.response.send_message(content="You've been added to the CTF group",ephemeral=True)

    @discord.ui.button(label="Quiet!", style=discord.ButtonStyle.red, emoji="❎", custom_id="remove")
    async def remove_callback(self,interaction,button):
        role_user = interaction.user
        ctfr = discord.utils.get(interaction.guild.roles, name=ctf_role)
        if ctfr != None:
            await role_user.remove_roles(ctfr)
            await interaction.response.send_message(content="You're no longer part of the CTF group",ephemeral=True)

async def create_channel(ctg_obj, ch_name, topic=""):
    chan = discord.utils.get(ctg_obj.channels, name=ch_name)
    if chan == None:
        chan = await ctg_obj.create_text_channel(ch_name,topic=topic)
    return chan

async def create_cat(guild, category_name):
    ctg = discord.utils.get(guild.categories, name=category_name)
    if ctg == None:
        ctg = await guild.create_category(category_name)
    return ctg

def check_bot_cat(message):
    cat, channel_name = get_cat_chan(message)
    if (message.author != client.user) and str(cat) == str(ctf_category) and (str(channel_name) != str(register_channel_name) and str(channel_name) != str(bot_channel_name)):
        return True
    else:
        return False

def check_chall_thread(message):
    cat, channel_name = get_cat_chan(message)
    if (message.author != client.user) and str(cat) == str(running_category) and (str(channel_name) != str(register_channel_name) and str(channel_name) != str(bot_channel_name)) and message.channel.type==discord.ChannelType.public_thread:
        return True
    else:
        return False

def check_ctfs_channels(message):
    cat, channel_name = get_cat_chan(message)
    if (message.author != client.user) and str(cat) == str(running_category) and (str(channel_name) != str(register_channel_name) and str(channel_name) != str(bot_channel_name)) and message.channel.type==discord.ChannelType.text:
        return True
    else:
        return False

def check_bot_channel(message):
    cat, channel_name = get_cat_chan(message)
    if ((str(cat) == ctf_category) and (str(channel_name)== bot_channel_name) and (message.author != client.user)):
        return True
    else:
        return False

async def init_setup():
    guilds = client.guilds
    for g in guilds:
        await initial_guild_setup(g)

async def initial_guild_setup(g):
   #create ctf bot chat cat
    ctf_ctg = await create_cat(g, ctf_category)
    reg_channel = discord.utils.get(ctf_ctg.channels, name=register_channel_name)
    if reg_channel == None:
        reg_channel = await create_channel(ctf_ctg, register_channel_name,"CTF Role registration channel")
        await reg_channel.send("This is the registration channel for the CTF role. If you select this you'll be pinged for all ctf related news")
        await reg_channel.send("Click here to setup your alerts and role.", view=RoleView())
    bot_channel = await create_channel(ctf_ctg, bot_channel_name,"Bot commands channel")

    #create running CTF cat and set perms
    ctg = await create_cat(g, running_category)
    await ctg.set_permissions(g.default_role, overwrite=set_everyone_perms())

    #re apply permissions on registration channel
    await reg_channel.set_permissions(g.default_role, overwrite=discord.PermissionOverwrite(send_messages=False))
    #create the ctf role
    await create_role(g, ctf_role)
    #re-add the view to keep it consistent
    client.add_view(RoleView())
    #create archive cat and set permissions
    archives_ctg = await create_cat(g, archive_category)
    await archives_ctg.set_permissions(g.default_role, overwrite=set_archives_perms())

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await init_setup()

@client.event
async def on_guild_join(guild):
    await initial_guild_setup(guild)

# Create new CTF
@client.command()
async def create(message, *, ctf_name):
    """Creates a new CTF channel."""
    if not check_bot_channel(message):
        await message.send("Use the **%s** channel for this" % bot_channel_name)
        return
    else:
        ctg = discord.utils.get(message.guild.categories, name=running_category)
        ctf_chann = await create_channel(ctg, ctf_name)

#Delete ctf channel
@client.command()
async def rmctf(message):
    """Deletes a CTF Channel. Be careful using this, only used for mistakes, otherwise archive the CTF"""
    if not check_ctfs_channels(message):
        await message.send("Use only on a CTF channel")
        return
    else:
        await message.channel.delete()

#Add new chall
@client.command()
async def add(message, *, chall_name):
    """Can only be used from within a CTF channel created by ctf_create. Creates a thread for challenge discussion."""
    cat, channel_name = get_cat_chan(message)
    if check_ctfs_channels(message):
        ths = [strip_status(t) for t in get_names(message.channel.threads)]
        if chall_name not in ths:
            th = await channel_name.create_thread(name="%s%s"%(unsolved_string,strip_status(chall_name)),type=discord.ChannelType.public_thread)

#Remove chall
@client.command()
async def rm(message):
    """Can only be used from within a chall channel created by ctf_addchall. Deletes a challenge thread."""
    cat, channel_name = get_cat_chan(message)
    if check_chall_thread(message):
        await message.channel.delete()

#Set credentials and pin
@client.command()
async def creds(message, login, password):
    """Sets and pins a message with the credentials for the CTF."""
    if check_ctfs_channels(message):
        cat, name = get_cat_chan(message)
        desc = "**CTF: %s** \n Login: %s \n Password: %s" % (name, login, password)
        emb = discord.Embed(description=desc)

        pinned = await message.channel.pins()
        if not pinned:
            msg = await message.send(embed=emb)
            await msg.pin()
        else:
            for f in pinned:
                if f.author == client.user:
                    await f.edit(embed=emb)

#Set channel as solved
@client.command()
async def solve(message):
    if check_chall_thread(message):
        if message.channel.type == discord.ChannelType.public_thread:
            uns_name = strip_status(str(message.channel.name))
            await message.channel.edit(name="%s%s" % (solved_string,uns_name))

#Set channel as unsolved
@client.command()
async def unsolve(message):
    if check_chall_thread(message):
        if message.channel.type == discord.ChannelType.public_thread:
            uns_name = strip_status(str(message.channel.name))
            await message.channel.edit(name="%s%s" % (unsolved_string,uns_name))

#List current challenges on this CTF
@client.command()
async def ls(message):
    """List current challenges and status"""
    if check_ctfs_channels(message):
        thrs = message.channel.threads
        if thrs:
            challs = []
            for t in thrs:
                challs.append(t.name)
            emby = discord.Embed(title="Current challs:")
            ls_text = ""
            for c in challs:
                ls_text = ("%s\n%s")%(ls_text,c)
            emby.description = ls_text
            await message.channel.send(embed=emby)

#Archive CTF as read only
@client.command()
async def archive(message):
    """Archives a CTF channel. Archives are Read Only."""
    if check_ctfs_channels(message):
        archive_ctg = discord.utils.get(message.guild.categories, name=archive_category)
        await message.channel.move(beginning=True,category=archive_ctg,sync_permissions=True)

client.run(TOKEN)