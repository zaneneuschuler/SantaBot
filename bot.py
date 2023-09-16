import discord
import aiohttp
import io
import os
import db
from dotenv import load_dotenv

load_dotenv()

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
            await ctx.respond(file=discord.File(data, f'{ctx.author.id}.{upload_ext}'), content=f'Hi {stepartist}!')
            db.put(ctx.author.id, stepartist)
            #DB expects author ID and then stepartist name

@santa.command(description="LET'S HECKING GOOOOOOOOOOOOOOOOOO")
async def hohoho(ctx):
    print(type(ctx.author.id))
    if (ctx.author.id != 262440960040894474) or (ctx.author.id != 84108714671345664): # TODO: also put this in .env
        await ctx.respond("You're not allowed to start the christmas season!")
    else:
        await ctx.respond("Ho ho ho! Be prepared to get your files...")
        # TODO: file distribution logic 

bot.run(os.getenv("CLIENT_TOKEN"))
