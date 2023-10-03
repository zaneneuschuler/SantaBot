import discord
import aiohttp
import io
import os
import db
import random
import shutil

from dotenv import load_dotenv

load_dotenv()

def testing_function(first, second):
    for i in range(len(first)):
        if first[i][0] == second[i][0]:
            return True
        else: 
            pass
    return False

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

devs = os.getenv("ADMIN_IDS").strip('][').split(', ') #take devs from ADMIN_IDS in .env and convert to a list of dev ids

bot = discord.Bot()
# Guilds go into .env as a string split by spaces
bot_guild_ids = os.getenv("GUILD_IDS").split(' ')


# create Slash Command group with bot.create_group
greetings = bot.create_group("greetings", "Greet people")

@greetings.command(description="Hi there!")
async def hello(ctx):
  await ctx.respond(f"Hello, {ctx.author}!")

@greetings.command(description="Bye there!")
async def bye(ctx):
  await ctx.respond(f"Bye, {ctx.author.id}!")

santa = bot.create_group("santa", "Secret santa things!")

@santa.command(description="Upload your skeleton!")
async def upload(ctx, file:discord.Attachment, stepartist:discord.SlashCommandOptionType.string):
    async with aiohttp.ClientSession() as session:
        async with session.get(file.url) as resp: #async grab file from discord's servers
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            upload_ext = file.url.split(".")[-1] # grab extension
            
            f = open(f'uploads/{ctx.author.id}.{upload_ext}', "wb")
            f.write(data.getbuffer()) #write datastream to file and close
            f.close()
            await ctx.respond("Your file has been submitted! Please await distribution time to see what presents you get! If you want to make changes to your file, feel free to reupload your file! :3", ephemeral=True)
            db.put(ctx.author.id, stepartist)
            #DB expects author ID and then stepartist name

@santa.command(description="LET'S HECKING GOOOOOOOOOOOOOOOOOO")
async def hohoho(ctx):
    if str(ctx.author.id) in os.getenv("ADMIN_IDS"): # TODO: also put this in .env
        await ctx.respond("Ho ho ho! Be prepared to get your files...", ephemeral=True)
        stepartists = db.get()
        stepartists_randomized = random.sample(stepartists, len(stepartists))
        shuffled = testing_function(stepartists,stepartists_randomized)
        while shuffled:
            print("Need to reshuffle!") #cursed. will literally not scale well at all.
            random.shuffle(stepartists_randomized)
            shuffled = testing_function(stepartists,stepartists_randomized)
        message_to_send = ""
        for i in range(len(stepartists)):
            santa = stepartists[i][0]
            lucky_boy_or_girl = stepartists_randomized[i][0]
            message_to_send += f'Stepartist {stepartists[i][1]} will get {stepartists_randomized[i][1]}\'s file!\n'
            new_file = shutil.copyfile(f'uploads/{lucky_boy_or_girl}.png', f'uploads/{stepartists[i][1]}present.png') #shouldn't hardcode in/out extensions, but fixable.
            user = await bot.fetch_user(santa)
            try: 
                await user.send(f"Here is your file! If you have any questions/concerns, feel free to message <@{devs[2]}>, and make sure to submit your file when you're done to him as well!  Ho ho ho!", file=discord.File(f'{new_file}'))
                os.remove(new_file)
            except:
                ctx.respond(f'Could not send file to {stepartists[i][1]}! File has been saved, please manually DM them!', ephemeral=True)


        await ctx.respond(message_to_send, ephemeral=True)

    else:
        await ctx.respond("Oops! You're not allowed to use this command!", ephemeral=True)


@santa.command(description="For internal testing purposes")
async def testing(ctx):
    
    await ctx.respond(f' ', ephemeral=True)


bot.run(os.getenv("CLIENT_TOKEN"))


